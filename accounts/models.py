from django.conf import settings
from django.db import models


class Profile(models.Model):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('booking_staff', 'Booking Staff'),
        ('fleet_manager', 'Fleet Manager'),
        ('administrator', 'Administrator'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'
