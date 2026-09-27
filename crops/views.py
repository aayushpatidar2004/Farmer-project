from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Crop, PlantImage
from .forms import CropForm, PlantImageForm


@login_required
def crop_list_view(request):
    """List all crops belonging to the logged-in farmer with search."""
    crops = Crop.objects.filter(farmer=request.user)
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()

    if search_query:
        crops = crops.filter(
            Q(crop_name__icontains=search_query) |
            Q(variety__icontains=search_query) |
            Q(notes__icontains=search_query)
        )

    if status_filter:
        crops = crops.filter(status=status_filter)

    context = {
        'crops': crops,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': Crop.STATUS_CHOICES,
        'total': Crop.objects.filter(farmer=request.user).count(),
    }
    return render(request, 'crops/list.html', context)


@login_required
def crop_add_view(request):
    """Add a new crop."""
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.farmer = request.user
            crop.save()
            messages.success(request, f"Crop '{crop.crop_name}' added successfully!")
            return redirect('crops:detail', pk=crop.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CropForm()

    return render(request, 'crops/add.html', {'form': form})


@login_required
def crop_detail_view(request, pk):
    """Crop detail page — farmer can only view their own crops."""
    crop = get_object_or_404(Crop, pk=pk, farmer=request.user)
    images = crop.images.all()
    return render(request, 'crops/detail.html', {'crop': crop, 'images': images})


@login_required
def crop_edit_view(request, pk):
    """Edit an existing crop."""
    crop = get_object_or_404(Crop, pk=pk, farmer=request.user)

    if request.method == 'POST':
        form = CropForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            messages.success(request, f"Crop '{crop.crop_name}' updated successfully!")
            return redirect('crops:detail', pk=crop.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CropForm(instance=crop)

    return render(request, 'crops/edit.html', {'form': form, 'crop': crop})


@login_required
def crop_delete_view(request, pk):
    """Delete a crop (POST only)."""
    crop = get_object_or_404(Crop, pk=pk, farmer=request.user)

    if request.method == 'POST':
        crop_name = crop.crop_name
        crop.delete()
        messages.success(request, f"Crop '{crop_name}' deleted successfully.")
        return redirect('crops:list')

    return render(request, 'crops/confirm_delete.html', {'crop': crop})


@login_required
def upload_image_view(request, crop_pk):
    """Upload a plant/crop image for a specific crop."""
    crop = get_object_or_404(Crop, pk=crop_pk, farmer=request.user)

    if request.method == 'POST':
        form = PlantImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.crop = crop
            img.save()
            messages.success(request, "Image uploaded successfully!")
            return redirect('crops:detail', pk=crop.pk)
        else:
            messages.error(request, "Image upload failed. Please check file type and size (max 5 MB).")
    else:
        form = PlantImageForm()

    return render(request, 'crops/upload_image.html', {'form': form, 'crop': crop})


@login_required
def delete_image_view(request, pk):
    """Delete a plant image (POST only)."""
    image = get_object_or_404(PlantImage, pk=pk, crop__farmer=request.user)

    if request.method == 'POST':
        crop_pk = image.crop.pk
        image.image.delete(save=False)  # Remove file from disk
        image.delete()
        messages.success(request, "Image deleted successfully.")
        return redirect('crops:detail', pk=crop_pk)

    return redirect('crops:list')


@login_required
def my_images_view(request):
    """Gallery of all images uploaded by the farmer."""
    images = PlantImage.objects.filter(crop__farmer=request.user).select_related('crop')
    return render(request, 'crops/my_images.html', {'images': images})
