from django.db import models
from services.models import Service
from django.utils import timezone

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    full_name = models.CharField(max_length=255)
    age = models.IntegerField()
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    note = models.TextField(blank=True, null=True)
    appointment_date = models.DateField(blank=True, null=True,default = timezone.now, db_index=True)
    appointment_time = models.TimeField(blank=True, null=True, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['appointment_date', 'appointment_time'],
                name='unique_appointment_slot',
                condition=~models.Q(status='cancelled')
            )
        ]

    def __str__(self):
        return f"Booking for {self.service.name} by {self.full_name}"
