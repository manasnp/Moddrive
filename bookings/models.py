from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from fleet.models import DrivingRoute, Vehicle


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, related_name='bookings')
    route = models.ForeignKey(DrivingRoute, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    customer_notes = models.TextField(blank=True)
    decision_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def rental_days(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 0

    def clean(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError('The end date must be on or after the start date.')

        conflicts = Booking.objects.filter(
            vehicle=self.vehicle,
            status__in=['pending', 'approved'],
            start_date__lte=self.end_date,
            end_date__gte=self.start_date,
        ).exclude(pk=self.pk)
        if conflicts.exists():
            raise ValidationError('This vehicle already has a request for the selected dates.')

    def calculate_price(self):
        base = self.vehicle.daily_price * Decimal(max(self.rental_days, 1))
        route_price = self.route.additional_price if self.route else Decimal('0')
        return base + route_price

    def save(self, *args, **kwargs):
        self.full_clean()
        self.estimated_price = self.calculate_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.customer.username} - {self.vehicle.name} ({self.status})'
