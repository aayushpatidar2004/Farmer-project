from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from crops.models import Crop
from soil.models import SoilData
from diseases.models import Disease
from market.models import MarketPrice
from accounts.models import FarmerProfile
from recommendations.engine import get_recommendations
from weather.services import get_weather_by_city
from .permissions import IsOwnerOrAdmin
from .serializers import (
    CropSerializer, SoilDataSerializer, DiseaseSerializer,
    MarketPriceSerializer, FarmerProfileSerializer,
)


# --------------------------------------------------------------------------
# Profile
# --------------------------------------------------------------------------

class ProfileAPIView(APIView):
    """GET /api/profile/ — return the authenticated user's profile."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.farmer_profile
        except FarmerProfile.DoesNotExist:
            return Response({'detail': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FarmerProfileSerializer(profile)
        return Response(serializer.data)


# --------------------------------------------------------------------------
# Crops
# --------------------------------------------------------------------------

class CropListCreateAPIView(generics.ListCreateAPIView):
    """GET /api/crops/ — list farmer's crops; POST to create."""
    serializer_class = CropSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Crop.objects.filter(farmer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)


class CropDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE /api/crops/<id>/"""
    serializer_class = CropSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        return Crop.objects.filter(farmer=self.request.user)


# --------------------------------------------------------------------------
# Diseases
# --------------------------------------------------------------------------

class DiseaseListAPIView(generics.ListAPIView):
    """GET /api/diseases/?search=q&crop=c"""
    serializer_class = DiseaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Disease.objects.all()
        search = self.request.query_params.get('search', '')
        crop = self.request.query_params.get('crop', '')
        if search:
            qs = qs.filter(
                Q(disease_name__icontains=search) | Q(crop_name__icontains=search)
            )
        if crop:
            qs = qs.filter(crop_name__icontains=crop)
        return qs


class DiseaseDetailAPIView(generics.RetrieveAPIView):
    """GET /api/diseases/<id>/"""
    serializer_class = DiseaseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Disease.objects.all()


# --------------------------------------------------------------------------
# Market Prices
# --------------------------------------------------------------------------

class MarketPriceListAPIView(generics.ListAPIView):
    """GET /api/market-prices/?crop_name=q&market=q&unit=u"""
    serializer_class = MarketPriceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = MarketPrice.objects.all()
        crop = self.request.query_params.get('crop_name', '')
        market = self.request.query_params.get('market', '')
        unit = self.request.query_params.get('unit', '')
        if crop:
            qs = qs.filter(crop_name__icontains=crop)
        if market:
            qs = qs.filter(market_name__icontains=market)
        if unit:
            qs = qs.filter(unit=unit)
        return qs


# --------------------------------------------------------------------------
# Recommendation
# --------------------------------------------------------------------------

class RecommendationAPIView(APIView):
    """
    POST /api/recommendation/
    Body: { soil_type, ph, nitrogen, phosphorus, potassium,
            temperature?, rainfall?, humidity? }
    Returns top 5 crop recommendations.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        required = ['ph', 'nitrogen', 'phosphorus', 'potassium']
        errors = {}
        for field in required:
            if field not in request.data:
                errors[field] = ['This field is required.']
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            inputs = {
                'soil_type': request.data.get('soil_type', ''),
                'ph': float(request.data['ph']),
                'nitrogen': float(request.data['nitrogen']),
                'phosphorus': float(request.data['phosphorus']),
                'potassium': float(request.data['potassium']),
            }
            for opt in ('temperature', 'rainfall', 'humidity'):
                val = request.data.get(opt)
                if val is not None:
                    inputs[opt] = float(val)
        except (ValueError, TypeError):
            return Response(
                {'detail': 'All numeric fields must be valid numbers.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        recommendations = get_recommendations(inputs, top_n=5)
        return Response({
            'inputs': inputs,
            'recommendations': recommendations,
            'disclaimer': (
                'Recommendations are for informational purposes only. '
                'Consult local agricultural experts before making farming decisions.'
            ),
        })


# --------------------------------------------------------------------------
# Weather
# --------------------------------------------------------------------------

class WeatherAPIView(APIView):
    """
    GET /api/weather/?city=CityName
    Returns current weather from Open-Meteo (free, no API key).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        city = request.query_params.get('city', '').strip()
        if not city:
            return Response(
                {'detail': 'city query parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        weather, location, error = get_weather_by_city(city)
        if error:
            return Response({'detail': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({
            'location': location,
            'weather': weather,
            'source': 'Open-Meteo (https://open-meteo.com) — Free, No API Key',
        })
