from django.db import models


class MarketPrice(models.Model):
    """Agricultural market price record."""

    UNIT_CHOICES = [
        ('per_kg', '₹/kg'),
        ('per_quintal', '₹/quintal'),
        ('per_tonne', '₹/tonne'),
        ('per_dozen', '₹/dozen'),
    ]

    crop_name = models.CharField(max_length=100, db_index=True)
    market_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='per_quintal')
    date = models.DateField(db_index=True)
    is_sample_data = models.BooleanField(
        default=False,
        help_text='True indicates this is demo/sample data, not a live price.'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'crop_name']
        verbose_name = 'Market Price'
        verbose_name_plural = 'Market Prices'

    def __str__(self):
        return (
            f"{self.crop_name} — {self.market_name} — "
            f"₹{self.price} {self.get_unit_display()} ({self.date})"
        )
