from django.urls import path

from . import views

app_name = "fleet"

urlpatterns = [
    path("", views.fleet_list, name="fleet_list"),
    path("routes/", views.route_list, name="route_list"),
    path("favorites/", views.favorite_list, name="favorite_list"),
    path("<int:vehicle_id>/", views.vehicle_detail, name="vehicle_detail"),
    path("<int:vehicle_id>/toggle_favorite/", views.toggle_favorite, name="toggle_favorite"),
]
