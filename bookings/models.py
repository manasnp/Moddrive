from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Booking(models.Model):
    STATUS_CHOICES = [  
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("denied", "Denied"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    vehicle = models.ForeignKey(
        "fleet.Vehicle",
        on_delete=models.PROTECT,
        related_name="bookings",
    )
    
    route = models.ForeignKey(
    "fleet.DrivingRoute",
    on_delete=models.SET_NULL,
    related_name="bookings",
    null=True,
    blank=True,
)

    start_date = models.DateField()
    end_date = models.DateField()

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    customer_notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ("-created_at",)

    def clean(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError(
                "The end date cannot be before the start date."
            )

        if (
            self.vehicle_id
            and self.start_date
            and self.end_date
            and self.status in ["pending", "approved"]
        ):
            conflicting_bookings = Booking.objects.filter(
                vehicle_id=self.vehicle_id,
                status__in=["pending", "approved"],
                start_date__lte=self.end_date,
                end_date__gte=self.start_date,
            ).exclude(pk=self.pk)

            if conflicting_bookings.exists():
                raise ValidationError(
                    "This vehicle is unavailable for the selected dates."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.customer.username} - "
            f"{self.vehicle} - "
            f"{self.status}"
        )