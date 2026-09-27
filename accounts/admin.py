from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import FarmerProfile


class FarmerProfileInline(admin.StackedInline):
    model = FarmerProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('phone', 'location', 'farm_name', 'farm_size', 'bio', 'profile_pic', 'role')


class CustomUserAdmin(UserAdmin):
    inlines = (FarmerProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_active', 'date_joined')
    list_filter = ('is_active', 'farmer_profile__role')

    def get_role(self, obj):
        try:
            return obj.farmer_profile.get_role_display()
        except FarmerProfile.DoesNotExist:
            return 'No Profile'
    get_role.short_description = 'Role'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
