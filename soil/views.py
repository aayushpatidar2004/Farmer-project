from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import SoilDataForm
from .models import SoilData


@login_required
def soil_list_view(request):
    """List all soil records for the current farmer."""
    records = SoilData.objects.filter(farmer=request.user)
    return render(request, 'soil/list.html', {'soil_records': records})


@login_required
def soil_add_view(request):
    """Add a new soil data record."""
    if request.method == 'POST':
        form = SoilDataForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.farmer = request.user
            record.save()
            messages.success(request, "Soil data saved successfully!")
            return redirect('soil:detail', pk=record.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = SoilDataForm()

    return render(request, 'soil/form.html', {'form': form, 'title': 'Add Soil Data'})


@login_required
def soil_detail_view(request, pk):
    """Show a single soil record with NumPy-based nutrient analysis."""
    record = get_object_or_404(SoilData, pk=pk, farmer=request.user)
    analysis = record.get_nutrient_analysis()
    ph_status, ph_color = record.get_ph_status()
    return render(request, 'soil/detail.html', {
        'soil_record': record,
        'analysis': analysis,
        'ph_status': ph_status,
        'ph_color': ph_color,
    })


@login_required
def soil_edit_view(request, pk):
    """Edit an existing soil record."""
    record = get_object_or_404(SoilData, pk=pk, farmer=request.user)

    if request.method == 'POST':
        form = SoilDataForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Soil data updated successfully!")
            return redirect('soil:detail', pk=record.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = SoilDataForm(instance=record)

    return render(request, 'soil/form.html', {'form': form, 'record': record, 'title': 'Edit Soil Data'})


@login_required
def soil_delete_view(request, pk):
    """Delete a soil record (POST only)."""
    record = get_object_or_404(SoilData, pk=pk, farmer=request.user)

    if request.method == 'POST':
        record.delete()
        messages.success(request, "Soil record deleted.")
        return redirect('soil:list')

    return render(request, 'soil/confirm_delete.html', {'record': record})
