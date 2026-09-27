from rest_framework import serializers
from django.contrib.auth.models import User

from accounts.models import FarmerProfile
from crops.models import Crop, PlantImage
from soil.models import SoilData
from diseases.models import Disease, Pesticide
from market.models import MarketPrice


class FarmerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = FarmerProfile
        fields = [
            'id', 'username', 'full_name', 'email',
            'phone', 'location', 'farm_name', 'farm_size',
            'bio', 'profile_pic', 'role', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username


class CropSerializer(serializers.ModelSerializer):
    farmer_username = serializers.CharField(source='farmer.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Crop
        fields = [
            'id', 'farmer_username', 'crop_name', 'crop_type', 'variety',
            'sowing_date', 'expected_harvest_date', 'land_area', 'area_unit',
            'soil_type', 'irrigation_type', 'status', 'status_display',
            'notes', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'farmer_username', 'status_display']


class PlantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantImage
        fields = ['id', 'crop', 'image', 'description', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class SoilDataSerializer(serializers.ModelSerializer):
    farmer_username = serializers.CharField(source='farmer.username', read_only=True)

    class Meta:
        model = SoilData
        fields = [
            'id', 'farmer_username', 'soil_type', 'ph',
            'nitrogen', 'phosphorus', 'potassium',
            'moisture', 'organic_matter', 'notes', 'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'farmer_username']


class PesticideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pesticide
        fields = [
            'id', 'name', 'pesticide_type', 'active_ingredient',
            'dosage', 'application_method', 'safety_notes',
        ]


class DiseaseSerializer(serializers.ModelSerializer):
    pesticides = PesticideSerializer(many=True, read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)

    class Meta:
        model = Disease
        fields = [
            'id', 'crop_name', 'disease_name', 'symptoms', 'causes',
            'prevention', 'treatment', 'severity', 'severity_display',
            'image', 'pesticides',
        ]


class MarketPriceSerializer(serializers.ModelSerializer):
    unit_display = serializers.CharField(source='get_unit_display', read_only=True)

    class Meta:
        model = MarketPrice
        fields = [
            'id', 'crop_name', 'market_name', 'location',
            'price', 'unit', 'unit_display', 'date',
            'is_sample_data', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']
