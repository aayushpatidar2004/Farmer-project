from django import forms
from .models import SoilData


class SoilDataForm(forms.ModelForm):
    """Form for entering soil analysis data."""

    class Meta:
        model = SoilData
        fields = [
            'soil_type', 'ph', 'nitrogen', 'phosphorus',
            'potassium', 'moisture', 'organic_matter', 'notes',
        ]
        widgets = {
            'soil_type': forms.Select(attrs={'class': 'form-select'}),
            'ph': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.01',
                'min': '0', 'max': '14', 'placeholder': '6.5',
            }),
            'nitrogen': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.01',
                'min': '0', 'placeholder': 'kg/ha',
            }),
            'phosphorus': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.01',
                'min': '0', 'placeholder': 'kg/ha',
            }),
            'potassium': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.01',
                'min': '0', 'placeholder': 'kg/ha',
            }),
            'moisture': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.01',
                'min': '0', 'max': '100', 'placeholder': '%',
            }),
            'organic_matter': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.01',
                'min': '0', 'max': '100', 'placeholder': '%',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Additional notes about the soil sample...',
            }),
        }

    def clean_ph(self):
        ph = self.cleaned_data.get('ph')
        if ph is not None and not (0 <= float(ph) <= 14):
            raise forms.ValidationError('pH must be between 0 and 14.')
        return ph

    def clean_moisture(self):
        m = self.cleaned_data.get('moisture')
        if m is not None and not (0 <= float(m) <= 100):
            raise forms.ValidationError('Moisture must be between 0 and 100%.')
        return m

    def clean_organic_matter(self):
        om = self.cleaned_data.get('organic_matter')
        if om is not None and not (0 <= float(om) <= 100):
            raise forms.ValidationError('Organic matter must be between 0 and 100%.')
        return om
