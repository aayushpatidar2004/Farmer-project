from django.contrib import admin
from .models import Crop, PlantImage


class PlantImageInline(admin.TabularInline):
    model = PlantImage
    extra = 0
    readonly_fields = ('uploaded_at',)


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('crop_name', 'crop_type', 'farmer', 'status', 'sowing_date', 'expected_harvest_date', 'created_at')
    list_filter = ('status', 'crop_type', 'soil_type', 'irrigation_type')
    search_fields = ('crop_name', 'variety', 'farmer__username', 'farmer__email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PlantImageInline]
    date_hierarchy = 'created_at'


@admin.register(PlantImage)
class PlantImageAdmin(admin.ModelAdmin):
    list_display = ('crop', 'description', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('crop__crop_name', 'description')
    readonly_fields = ('uploaded_at',)
