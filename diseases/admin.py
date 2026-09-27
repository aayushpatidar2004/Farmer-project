from django.contrib import admin
from .models import Disease, Pesticide


class PesticideInline(admin.TabularInline):
    model = Pesticide
    extra = 1
    fields = ('name', 'pesticide_type', 'active_ingredient', 'dosage', 'application_method', 'safety_notes')


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('disease_name', 'crop_name', 'severity', 'created_at')
    list_filter = ('severity', 'crop_name')
    search_fields = ('disease_name', 'crop_name', 'symptoms')
    readonly_fields = ('created_at',)
    inlines = [PesticideInline]


@admin.register(Pesticide)
class PesticideAdmin(admin.ModelAdmin):
    list_display = ('name', 'pesticide_type', 'disease', 'active_ingredient')
    list_filter = ('pesticide_type',)
    search_fields = ('name', 'active_ingredient', 'disease__disease_name')
