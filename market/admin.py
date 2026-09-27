from django.contrib import admin
from .models import MarketPrice


@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ('crop_name', 'market_name', 'location', 'price', 'unit', 'date', 'is_sample_data')
    list_filter = ('unit', 'is_sample_data', 'date')
    search_fields = ('crop_name', 'market_name', 'location')
    date_hierarchy = 'date'
    readonly_fields = ('created_at',)
    list_editable = ('price',)
