from django.contrib import admin

from .models import DrivingRoute, Favorite, Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "manufacturer",
        "model_year",
        "vehicle_type",
        "transmission",
        "daily_price",
        "is_available",
    )

    list_filter = (
        "vehicle_type",
        "transmission",
        "is_available",
    )

    search_fields = (
        "name",
        "manufacturer",
    )


@admin.register(DrivingRoute)
class DrivingRouteAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "location",
        "distance_miles",
        "estimated_hours",
        "additional_price",
    )

    search_fields = (
        "name",
        "location",
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "vehicle",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "user__username",
        "vehicle__name",
    )
