from django.db import models


class Disease(models.Model):
    """Crop disease database entry."""

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    crop_name = models.CharField(max_length=100, db_index=True)
    disease_name = models.CharField(max_length=200)
    symptoms = models.TextField()
    causes = models.TextField()
    prevention = models.TextField()
    treatment = models.TextField()
    severity = models.CharField(
        max_length=10, choices=SEVERITY_CHOICES, default='medium'
    )
    image = models.ImageField(
        upload_to='disease_images/', null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['crop_name', 'disease_name']
        verbose_name = 'Disease'
        verbose_name_plural = 'Diseases'

    def __str__(self):
        return f"{self.disease_name} ({self.crop_name})"

    def get_severity_badge_class(self):
        mapping = {
            'low': 'bg-success',
            'medium': 'bg-warning text-dark',
            'high': 'bg-danger',
            'critical': 'bg-dark',
        }
        return mapping.get(self.severity, 'bg-secondary')


class Pesticide(models.Model):
    """Pesticide / treatment information linked to a Disease."""

    PESTICIDE_TYPE_CHOICES = [
        ('insecticide', 'Insecticide'),
        ('fungicide', 'Fungicide'),
        ('herbicide', 'Herbicide'),
        ('bactericide', 'Bactericide'),
        ('nematicide', 'Nematicide'),
        ('organic', 'Organic / Biopesticide'),
    ]

    disease = models.ForeignKey(
        Disease, on_delete=models.CASCADE, related_name='pesticides'
    )
    name = models.CharField(max_length=200)
    pesticide_type = models.CharField(max_length=20, choices=PESTICIDE_TYPE_CHOICES)
    active_ingredient = models.CharField(max_length=200, blank=True)
    dosage = models.CharField(
        max_length=200, help_text='Application dosage / concentration'
    )
    application_method = models.TextField()
    safety_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pesticide'
        verbose_name_plural = 'Pesticides'

    def __str__(self):
        return f"{self.name} for {self.disease.disease_name}"
