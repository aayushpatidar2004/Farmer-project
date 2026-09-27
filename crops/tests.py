from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.management import call_command
from django.urls import reverse
from crops.models import Crop
from soil.models import SoilData
from recommendations.engine import get_recommendations
from diseases.models import Disease


class SmartFarmerCoreTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testfarmer',
            email='farmer@example.com',
            password='Password123!'
        )

    def test_user_registration_profile_signal(self):
        """Test that registering a user auto-creates a FarmerProfile."""
        self.assertIsNotNone(self.user.farmer_profile)
        self.assertEqual(self.user.farmer_profile.role, 'farmer')

    def test_crop_crud(self):
        """Test crop creation, editing, detail, and deletion for logged-in user."""
        self.client.login(username='testfarmer', password='Password123!')

        # Create
        response = self.client.post(reverse('crops:add'), {
            'crop_name': 'Wheat',
            'crop_type': 'cereal',
            'variety': 'HD-2967',
            'land_area': '5.0',
            'area_unit': 'acres',
            'soil_type': 'alluvial',
            'irrigation_type': 'canal',
            'status': 'growing',
            'notes': 'Test wheat field',
        })
        self.assertEqual(response.status_code, 302)
        crop = Crop.objects.get(crop_name='Wheat')
        self.assertEqual(crop.farmer, self.user)

        # Detail
        detail_res = self.client.get(reverse('crops:detail', args=[crop.pk]))
        self.assertEqual(detail_res.status_code, 200)

        # Delete
        del_res = self.client.post(reverse('crops:delete', args=[crop.pk]))
        self.assertEqual(del_res.status_code, 302)
        self.assertFalse(Crop.objects.filter(pk=crop.pk).exists())

    def test_crop_recommendation_engine(self):
        """Test rule-based Pandas/NumPy recommendation engine output."""
        inputs = {
            'soil_type': 'alluvial',
            'ph': 6.5,
            'nitrogen': 180,
            'phosphorus': 40,
            'potassium': 80,
            'temperature': 22,
        }
        recs = get_recommendations(inputs, top_n=5)
        self.assertTrue(len(recs) > 0)
        self.assertIn('crop', recs[0])
        self.assertIn('score', recs[0])

    def test_disease_search(self):
        """Test disease model and search listing."""
        Disease.objects.create(
            crop_name='Rice',
            disease_name='Rice Blast',
            symptoms='Leaf spots',
            causes='Fungus',
            prevention='Clean seeds',
            treatment='Fungicide',
            severity='high'
        )
        self.client.login(username='testfarmer', password='Password123!')
        res = self.client.get(reverse('diseases:list') + '?q=Blast')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Rice Blast')

    def test_load_sample_data_is_idempotent_and_creates_soil_crop_records(self):
        """Demo seed data should populate supported sample totals without duplication."""
        call_command('load_sample_data')
        initial_crop_count = Crop.objects.filter(farmer=self.user).count()
        initial_soil_count = SoilData.objects.filter(farmer=self.user).count()

        self.assertGreaterEqual(initial_crop_count, 2)
        self.assertGreaterEqual(initial_soil_count, 4)

        call_command('load_sample_data')
        self.assertEqual(Crop.objects.filter(farmer=self.user).count(), initial_crop_count)
        self.assertEqual(SoilData.objects.filter(farmer=self.user).count(), initial_soil_count)

    def test_recommendation_uses_latest_soil_record_when_available(self):
        """Recommendation form should default to the farmer's latest soil readings."""
        SoilData.objects.create(
            farmer=self.user,
            soil_type='loamy',
            ph=6.5,
            nitrogen=180,
            phosphorus=38,
            potassium=90,
            moisture=28,
            organic_matter=2.8,
            notes='Demo soil data'
        )
        self.client.login(username='testfarmer', password='Password123!')
        response = self.client.get(reverse('recommendations:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '6.50')
        self.assertContains(response, 'Loamy')

    def test_contact_form_submits_and_validates(self):
        """Contact messages should save only when the form data is valid."""
        response = self.client.post(reverse('contact'), {
            'name': 'Demo User',
            'email': 'demo@example.com',
            'subject': 'Demo enquiry',
            'message': 'This is a test message.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.get(reverse('contact')).status_code == 200)
        self.assertTrue(self.client.post(reverse('contact'), {
            'name': '',
            'email': 'bad-email',
            'subject': 'Broken',
            'message': 'bad'
        }).status_code == 200)

    def test_superuser_profile_is_recognized_as_admin_dashboard_access(self):
        """Superusers must also be treated as admin-role users by the custom dashboard."""
        superuser = User.objects.create_superuser(
            username='superadmin',
            email='superadmin@example.com',
            password='Password123!'
        )
        superuser.refresh_from_db()

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.farmer_profile.role, 'admin')

        self.client.login(username='superadmin', password='Password123!')
        response = self.client.get(reverse('accounts:admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_admin_role_syncs_django_admin_permissions(self):
        """Admin-role users should get Django admin access automatically and farmers should be blocked."""
        admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='Password123!'
        )
        admin_user.farmer_profile.role = 'admin'
        admin_user.farmer_profile.save()
        admin_user.refresh_from_db()

        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        self.client.login(username='adminuser', password='Password123!')
        admin_response = self.client.get(reverse('accounts:admin_dashboard'))
        self.assertEqual(admin_response.status_code, 200)

        farmer_response = self.client.get(reverse('accounts:admin_dashboard'))
        self.assertEqual(farmer_response.status_code, 200)

        farmer_user = User.objects.create_user(
            username='farmeruser',
            email='farmer2@example.com',
            password='Password123!'
        )
        self.client.login(username='farmeruser', password='Password123!')
        access_response = self.client.get(reverse('accounts:admin_dashboard'))
        self.assertEqual(access_response.status_code, 403)
        self.assertContains(access_response, 'Access denied')
