from django.contrib import admin

from .models import DrivingRoute, Favorite, Vehicle

admin.site.register(Vehicle)
admin.site.register(DrivingRoute)
admin.site.register(Favorite)
