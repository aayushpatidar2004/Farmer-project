from django import forms
from .models import MarketPrice


class MarketPriceForm(forms.ModelForm):
    """Form for adding/editing a market price entry."""

    class Meta:
        model = MarketPrice
        fields = ['crop_name', 'market_name', 'location', 'price', 'unit', 'date', 'is_sample_data']
        widgets = {
            'crop_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Wheat'}),
            'market_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Azadpur Mandi'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Delhi'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_sample_data': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
