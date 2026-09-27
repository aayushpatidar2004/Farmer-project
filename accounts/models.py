from django.db import models
from django.contrib.auth.models import User


class FarmerProfile(models.Model):
    """Extended profile for all users (farmers and admins)."""

    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='farmer_profile'
    )
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=200, blank=True)
    farm_name = models.CharField(max_length=200, blank=True)
    farm_size = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text='Farm size in acres'
    )
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics/', null=True, blank=True
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='farmer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Farmer Profile'
        verbose_name_plural = 'Farmer Profiles'

    def __str__(self):
        name = self.user.get_full_name() or self.user.username
        return f"{name} ({self.get_role_display()})"

    @property
    def is_farmer(self):
        return self.role == 'farmer'

    @property
    def is_admin_role(self):
        return self.role == 'admin'

    @property
    def display_name(self):
        return self.user.get_full_name() or self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
