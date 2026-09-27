from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .services import get_weather_by_city


@login_required
def dashboard_view(request):
    """Weather dashboard — farmer enters city and gets current conditions."""
    weather = None
    location = None
    error = None
    city = ''

    if request.method == 'GET' and request.GET.get('city'):
        city = request.GET.get('city', '').strip()
        weather, location, error = get_weather_by_city(city)

    return render(request, 'weather/dashboard.html', {
        'weather': weather,
        'location': location,
        'error': error,
        'city': city,
    })
