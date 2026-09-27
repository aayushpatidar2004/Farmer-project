from django.db import models
from django.contrib.auth.models import User
import numpy as np


class SoilData(models.Model):
    """Soil analysis record entered by a farmer."""

    SOIL_TYPE_CHOICES = [
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

    farmer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='soil_records'
    )
    soil_type = models.CharField(max_length=20, choices=SOIL_TYPE_CHOICES)
    ph = models.DecimalField(
        max_digits=4, decimal_places=2,
        help_text='Soil pH (0–14). Optimal range: 6.0–7.5'
    )
    nitrogen = models.DecimalField(
        max_digits=8, decimal_places=2,
        help_text='Available Nitrogen in kg/ha'
    )
    phosphorus = models.DecimalField(
        max_digits=8, decimal_places=2,
        help_text='Available Phosphorus in kg/ha'
    )
    potassium = models.DecimalField(
        max_digits=8, decimal_places=2,
        help_text='Available Potassium in kg/ha'
    )
    moisture = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text='Soil moisture percentage (0–100)'
    )
    organic_matter = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text='Organic matter percentage (0–100)'
    )
    notes = models.TextField(blank=True)
    is_sample_data = models.BooleanField(
        default=False,
        help_text='True indicates this is demo/sample data and not a production soil record.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Soil Data'
        verbose_name_plural = 'Soil Data Records'

    def __str__(self):
        return (
            f"{self.get_soil_type_display()} soil — "
            f"{self.farmer.username} ({self.created_at.strftime('%Y-%m-%d')})"
        )

    def get_ph_status(self):
        """Return (label, Bootstrap color class) based on pH value."""
        ph = float(self.ph)
        if ph < 5.5:
            return 'Strongly Acidic', 'danger'
        elif ph < 6.0:
            return 'Acidic', 'warning'
        elif ph <= 7.5:
            return 'Neutral (Optimal)', 'success'
        elif ph <= 8.5:
            return 'Alkaline', 'warning'
        else:
            return 'Strongly Alkaline', 'danger'

    def get_nutrient_analysis(self):
        """
        Use NumPy to compute normalised nutrient scores relative to
        general crop production standards.
        Returns a dict with nitrogen, phosphorus, and potassium sub-dicts.
        """
        values = np.array(
            [float(self.nitrogen), float(self.phosphorus), float(self.potassium)]
        )
        # Typical adequate levels for most field crops (kg/ha)
        standards = np.array([280.0, 25.0, 120.0])
        ratios = np.clip(values / standards * 100, 0, 150)

        def label(r):
            if r < 50:
                return 'Low', 'danger'
            elif r < 80:
                return 'Moderate', 'warning'
            elif r <= 120:
                return 'Optimal', 'success'
            else:
                return 'High', 'info'

        n_lbl, n_cls = label(ratios[0])
        p_lbl, p_cls = label(ratios[1])
        k_lbl, k_cls = label(ratios[2])

        return {
            'nitrogen': {
                'value': float(self.nitrogen),
                'percentage': min(round(float(ratios[0]), 1), 100),
                'status': n_lbl,
                'color': n_cls,
            },
            'phosphorus': {
                'value': float(self.phosphorus),
                'percentage': min(round(float(ratios[1]), 1), 100),
                'status': p_lbl,
                'color': p_cls,
            },
            'potassium': {
                'value': float(self.potassium),
                'percentage': min(round(float(ratios[2]), 1), 100),
                'status': k_lbl,
                'color': k_cls,
            },
        }
