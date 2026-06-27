from django.db import models
from cloudinary.models import CloudinaryField

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.name
