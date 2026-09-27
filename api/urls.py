from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Profile
    path('profile/', views.ProfileAPIView.as_view(), name='profile'),
    # Crops
    path('crops/', views.CropListCreateAPIView.as_view(), name='crop-list'),
    path('crops/<int:pk>/', views.CropDetailAPIView.as_view(), name='crop-detail'),
    # Diseases
    path('diseases/', views.DiseaseListAPIView.as_view(), name='disease-list'),
    path('diseases/<int:pk>/', views.DiseaseDetailAPIView.as_view(), name='disease-detail'),
    # Market Prices
    path('market-prices/', views.MarketPriceListAPIView.as_view(), name='market-price-list'),
    # Recommendation Engine
    path('recommendation/', views.RecommendationAPIView.as_view(), name='recommendation'),
    # Weather (Open-Meteo)
    path('weather/', views.WeatherAPIView.as_view(), name='weather'),
]
