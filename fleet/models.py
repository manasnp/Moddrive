from django.conf import settings
from django.db import models


class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ("jdm", "JDM"),
        ("classic", "Classic"),
        ("offroad", "Off-Road"),
    ]

    TRANSMISSION_TYPES = [
        ("automatic", "Automatic"),
        ("manual", "Manual"),
    ]

    name = models.CharField(
        max_length=120,
    )

    manufacturer = models.CharField(
        max_length=100,
    )

    model_year = models.PositiveIntegerField()

    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPES,
    )

    transmission = models.CharField(
        max_length=20,
        choices=TRANSMISSION_TYPES,
    )

    daily_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    description = models.TextField()

    modifications = models.TextField(
        blank=True,
    )

    image_url = models.URLField(
        blank=True,
    )

    is_available = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["name"]

    def is_available_for(self, start_date, end_date):
        if not self.is_available:
            return False

        conflicting_bookings = self.bookings.filter(
            status__in=["pending", "approved"],
            start_date__lte=end_date,
            end_date__gte=start_date,
        )

        return not conflicting_bookings.exists()

    def __str__(self):
        return (
            f"{self.model_year} "
            f"{self.manufacturer} "
            f"{self.name}"
        )


class DrivingRoute(models.Model):
    name = models.CharField(
        max_length=120,
    )

    location = models.CharField(
        max_length=120,
    )

    description = models.TextField()

    distance_miles = models.PositiveIntegerField()

    estimated_hours = models.DecimalField(
        max_digits=4,
        decimal_places=1,
    )

    additional_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    image_url = models.URLField(
        blank=True,
    )

    vehicles = models.ManyToManyField(
        Vehicle,
        related_name="routes",
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="favorited_by",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "vehicle"],
                name="unique_user_vehicle_favorite",
            )
        ]

    def __str__(self):
        return f"{self.user.username} likes {self.vehicle.name}"