from django import forms
from .models import Crop, PlantImage


class CropForm(forms.ModelForm):
    """Form for creating and editing a Crop record."""

    class Meta:
        model = Crop
        fields = [
            'crop_name', 'crop_type', 'variety', 'sowing_date',
            'expected_harvest_date', 'land_area', 'area_unit',
            'soil_type', 'irrigation_type', 'status', 'notes',
        ]
        widgets = {
            'crop_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Wheat, Rice, Tomato'}),
            'crop_type': forms.Select(attrs={'class': 'form-select'}),
            'variety': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. HD-2967, Pusa Basmati'}),
            'sowing_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expected_harvest_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'land_area': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'area_unit': forms.Select(attrs={'class': 'form-select'}),
            'soil_type': forms.Select(attrs={'class': 'form-select'}),
            'irrigation_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes...'}),
        }


class PlantImageForm(forms.ModelForm):
    """Form for uploading a plant/crop image."""

    class Meta:
        model = PlantImage
        fields = ['image', 'description']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/jpeg,image/png,image/webp'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe what is shown in this image...',
            }),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            from django.conf import settings
            import os
            ext = os.path.splitext(image.name)[1].lower().lstrip('.')
            if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
                raise forms.ValidationError(
                    f"Unsupported file type '.{ext}'. "
                    f"Allowed: {', '.join(settings.ALLOWED_IMAGE_EXTENSIONS)}"
                )
            if image.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(
                    f"Image file is too large. Maximum size is "
                    f"{settings.MAX_UPLOAD_SIZE // (1024*1024)} MB."
                )
        return image
