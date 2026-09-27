from django.contrib import admin
from .models import SoilData


@admin.register(SoilData)
class SoilDataAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'soil_type', 'ph', 'nitrogen', 'phosphorus', 'potassium', 'moisture', 'created_at')
    list_filter = ('soil_type', 'created_at')
    search_fields = ('farmer__username', 'farmer__email')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
