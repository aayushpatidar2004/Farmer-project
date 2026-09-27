from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Disease, Pesticide


@login_required
def disease_list_view(request):
    """List/search diseases by crop name or disease name."""
    diseases = Disease.objects.all()
    search_query = request.GET.get('q', '').strip()
    crop_filter = request.GET.get('crop', '').strip()

    if search_query:
        diseases = diseases.filter(
            Q(disease_name__icontains=search_query) |
            Q(crop_name__icontains=search_query) |
            Q(symptoms__icontains=search_query)
        )

    if crop_filter:
        diseases = diseases.filter(crop_name__icontains=crop_filter)

    # Build unique crop list for filter dropdown
    crop_names = Disease.objects.values_list('crop_name', flat=True).distinct().order_by('crop_name')

    return render(request, 'diseases/list.html', {
        'diseases': diseases,
        'search_query': search_query,
        'crop_filter': crop_filter,
        'crop_names': crop_names,
    })


@login_required
def disease_detail_view(request, pk):
    """Detailed disease view with associated pesticide/treatment information."""
    disease = get_object_or_404(Disease, pk=pk)
    pesticides = disease.pesticides.all()
    return render(request, 'diseases/detail.html', {
        'disease': disease,
        'pesticides': pesticides,
    })
