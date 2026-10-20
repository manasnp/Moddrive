from django.db import models
from django.conf import settings

# Include a birthdate field using a separate model called UserProfile

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    birthdate = models.DateField()

    def __str__(self):
        return f"{self.user.username}'s profile"