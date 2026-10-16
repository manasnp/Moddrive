from django.conf import settings
from django.db import models


class Vehicle(models.Model):
    TYPE_CHOICES = [
        ('coupe', 'Coupe'),
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('truck', 'Truck'),
    ]
    TRANSMISSION_CHOICES = [('manual', 'Manual'), ('automatic', 'Automatic')]

    name = models.CharField(max_length=120)
    vehicle_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    description = models.TextField()
    modifications = models.TextField()
    maintenance_status = models.CharField(max_length=120, default='Inspected and ready')
    daily_price = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField(blank=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class DrivingRoute(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    description = models.TextField()
    distance_miles = models.PositiveIntegerField()
    estimated_hours = models.DecimalField(max_digits=4, decimal_places=1)
    additional_price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    image_url = models.URLField(blank=True)
    vehicles = models.ManyToManyField(Vehicle, related_name='routes', blank=True)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'vehicle'], name='unique_user_vehicle_favorite')
        ]

    def __str__(self):
        return f'{self.user.username} likes {self.vehicle.name}'
