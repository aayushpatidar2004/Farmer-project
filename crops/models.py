from django.db import models
from django.contrib.auth.models import User


class Crop(models.Model):
    """Represents a crop managed by a farmer."""

    CROP_TYPE_CHOICES = [
        ('cereal', 'Cereal'),
        ('vegetable', 'Vegetable'),
        ('fruit', 'Fruit'),
        ('legume', 'Legume'),
        ('oilseed', 'Oilseed'),
        ('cash_crop', 'Cash Crop'),
        ('spice', 'Spice'),
        ('other', 'Other'),
    ]

    SOIL_TYPE_CHOICES = [
        ('alluvial', 'Alluvial'),
        ('black', 'Black (Regur)'),
        ('red', 'Red'),
        ('laterite', 'Laterite'),
        ('sandy', 'Sandy'),
        ('loamy', 'Loamy'),
        ('clay', 'Clay'),
        ('other', 'Other'),
    ]

    IRRIGATION_TYPE_CHOICES = [
        ('drip', 'Drip Irrigation'),
        ('sprinkler', 'Sprinkler'),
        ('flood', 'Flood'),
        ('rain_fed', 'Rain Fed'),
        ('canal', 'Canal'),
        ('well', 'Well/Borewell'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('growing', 'Growing'),
        ('ready', 'Ready for Harvest'),
        ('harvested', 'Harvested'),
    ]

    AREA_UNIT_CHOICES = [
        ('acres', 'Acres'),
        ('hectares', 'Hectares'),
        ('bigha', 'Bigha'),
        ('sq_meters', 'Square Meters'),
    ]

    farmer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='crops'
    )
    crop_name = models.CharField(max_length=100)
    crop_type = models.CharField(
        max_length=20, choices=CROP_TYPE_CHOICES, default='other'
    )
    variety = models.CharField(max_length=100, blank=True)
    sowing_date = models.DateField(null=True, blank=True)
    expected_harvest_date = models.DateField(null=True, blank=True)
    land_area = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    area_unit = models.CharField(
        max_length=20, choices=AREA_UNIT_CHOICES, default='acres'
    )
    soil_type = models.CharField(
        max_length=20, choices=SOIL_TYPE_CHOICES, default='other'
    )
    irrigation_type = models.CharField(
        max_length=20, choices=IRRIGATION_TYPE_CHOICES, default='rain_fed'
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='planned'
    )
    notes = models.TextField(blank=True)
    is_sample_data = models.BooleanField(
        default=False,
        help_text='True indicates this is demo/sample data and not a real crop record.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Crop'
        verbose_name_plural = 'Crops'

    def __str__(self):
        return f"{self.crop_name} — {self.farmer.username}"

    def get_status_badge_class(self):
        mapping = {
            'planned': 'bg-secondary',
            'growing': 'bg-success',
            'ready': 'bg-warning text-dark',
            'harvested': 'bg-info',
        }
        return mapping.get(self.status, 'bg-secondary')


class PlantImage(models.Model):
    """Photo uploaded by the farmer for a specific crop."""

    crop = models.ForeignKey(
        Crop, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='plant_images/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Plant Image'
        verbose_name_plural = 'Plant Images'

    def __str__(self):
        return f"Image — {self.crop.crop_name} ({self.uploaded_at.strftime('%Y-%m-%d')})"
