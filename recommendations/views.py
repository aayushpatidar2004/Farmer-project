from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from soil.models import SoilData
from .engine import get_recommendations
from .forms import RecommendationForm


@login_required
def recommendation_view(request):
    """
    Crop recommendation page.
    Prefills from the latest real SoilData entry when available, then runs the Pandas/NumPy engine.
    """
    latest_soil = None
    if request.user.is_authenticated:
        latest_soil = SoilData.objects.filter(farmer=request.user).order_by('-created_at').first()

    initial_data = {}
    if latest_soil:
        initial_data = {
            'soil_type': latest_soil.soil_type,
            'ph': latest_soil.ph,
            'nitrogen': latest_soil.nitrogen,
            'phosphorus': latest_soil.phosphorus,
            'potassium': latest_soil.potassium,
        }

    form = RecommendationForm(initial=initial_data)
    recommendations = []
    show_results = False
    form_data = {}

    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            inputs = {
                "soil_type": cd.get("soil_type", ""),
                "ph": float(cd["ph"]),
                "nitrogen": float(cd["nitrogen"]),
                "phosphorus": float(cd["phosphorus"]),
                "potassium": float(cd["potassium"]),
                "temperature": float(cd["temperature"]) if cd.get("temperature") is not None else None,
                "rainfall": float(cd["rainfall"]) if cd.get("rainfall") is not None else None,
                "humidity": float(cd["humidity"]) if cd.get("humidity") is not None else None,
            }
            inputs = {k: v for k, v in inputs.items() if v is not None or k in ("soil_type", "ph", "nitrogen", "phosphorus", "potassium")}

            recommendations = get_recommendations(inputs, top_n=5)
            show_results = True
            form_data = cd

    return render(request, 'recommendations/index.html', {
        'form': form,
        'recommendations': recommendations,
        'show_results': show_results,
        'form_data': form_data,
        'latest_soil': latest_soil,
    })
