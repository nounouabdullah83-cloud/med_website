from django.db import models
from services.models import Service
from decimal import Decimal

class BookingStatistic(models.Model):
    date = models.DateField(db_index=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='statistics')
    completed_count = models.IntegerField(default=0)
    cancelled_count = models.IntegerField(default=0)
    total_revenues = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        unique_together = ('date', 'service')

    def __str__(self):
        return f"Stats for {self.service.name} on {self.date}"

        