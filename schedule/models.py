from django.db import models

class BusinessDay(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    day = models.IntegerField(choices=DAYS_OF_WEEK, unique=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        day_name = dict(self.DAYS_OF_WEEK).get(self.day)
        if self.is_closed:
            return f"{day_name}: Closed"
        return f"{day_name}: {self.opening_time} - {self.closing_time}"

    class Meta:
        ordering = ['day']
