from django import forms


SOIL_TYPE_CHOICES = [
    ('', '— Select Soil Type —'),
    ('alluvial', 'Alluvial'),
    ('black', 'Black (Regur)'),
    ('red', 'Red'),
    ('laterite', 'Laterite'),
    ('sandy', 'Sandy'),
    ('loamy', 'Loamy'),
    ('clay', 'Clay'),
    ('peaty', 'Peaty'),
    ('other', 'Other'),
]


class RecommendationForm(forms.Form):
    """Input form for the crop recommendation engine."""

    soil_type = forms.ChoiceField(
        choices=SOIL_TYPE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Soil Type',
    )
    ph = forms.DecimalField(
        min_value=0, max_value=14, decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'step': '0.01',
            'placeholder': 'e.g. 6.5',
        }),
        label='Soil pH',
    )
    nitrogen = forms.DecimalField(
        min_value=0, decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'step': '0.1', 'placeholder': 'kg/ha',
        }),
        label='Nitrogen (N) kg/ha',
    )
    phosphorus = forms.DecimalField(
        min_value=0, decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'step': '0.1', 'placeholder': 'kg/ha',
        }),
        label='Phosphorus (P) kg/ha',
    )
    potassium = forms.DecimalField(
        min_value=0, decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'step': '0.1', 'placeholder': 'kg/ha',
        }),
        label='Potassium (K) kg/ha',
    )
    temperature = forms.DecimalField(
        min_value=-10, max_value=55, decimal_places=1,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'step': '0.1', 'placeholder': '°C (optional)',
        }),
        label='Average Temperature (°C)',
    )
    rainfall = forms.DecimalField(
        min_value=0, decimal_places=1,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'step': '1', 'placeholder': 'mm/month (optional)',
        }),
        label='Average Monthly Rainfall (mm)',
    )
    humidity = forms.DecimalField(
        min_value=0, max_value=100, decimal_places=1,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'step': '1', 'placeholder': '% (optional)',
        }),
        label='Average Humidity (%)',
    )
