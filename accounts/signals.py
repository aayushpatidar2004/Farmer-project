from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import FarmerProfile


@receiver(post_save, sender=User)
def create_farmer_profile(sender, instance, created, **kwargs):
    """Automatically create a FarmerProfile when a new User is created."""
    if created:
        FarmerProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=FarmerProfile)
def sync_admin_role_permissions(sender, instance, **kwargs):
    """Keep Django admin permissions aligned with the profile role without demoting superusers."""
    user = instance.user

    if user.is_superuser:
        desired_staff = True
        desired_superuser = True
    elif instance.role == 'admin':
        desired_staff = True
        desired_superuser = False
    else:
        desired_staff = False
        desired_superuser = False

    if user.is_staff != desired_staff or user.is_superuser != desired_superuser:
        User.objects.filter(pk=instance.user_id).update(
            is_staff=desired_staff,
            is_superuser=desired_superuser,
        )


@receiver(post_save, sender=User)
def save_farmer_profile(sender, instance, **kwargs):
    """Keep profile role aligned when Django admin flags change on the user."""
    if kwargs.get('raw', False):
        return

    profile = getattr(instance, 'farmer_profile', None)
    if profile is None:
        return

    desired_role = 'admin' if instance.is_staff or instance.is_superuser else 'farmer'
    if profile.role != desired_role:
        FarmerProfile.objects.filter(pk=profile.pk).update(role=desired_role)
