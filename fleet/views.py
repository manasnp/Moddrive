from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import VehicleFilterForm
from .models import Vehicle, DrivingRoute, Favorite

def home(request):
    featured_vehicles = Vehicle.objects.filter(
        is_available=True
    )[:4]

    return render(
        request,
        "home.html",
        {
            "featured_vehicles": featured_vehicles,
        },
    )
def fleet_list(request):
    vehicles = Vehicle.objects.filter(is_available=True)

    form = VehicleFilterForm(request.GET or None)
    
    if form.is_valid():
        search = form.cleaned_data.get("search")
        vehicle_type = form.cleaned_data.get("vehicle_type")
        transmission = form.cleaned_data.get("transmission")
        maximum_price = form.cleaned_data.get("maximum_price")


        if search:
            vehicles = vehicles.filter(
                Q(name__icontains=search) | Q(manufacturer__icontains=search) | Q(description__icontains=search)
            )

        if vehicle_type:
            vehicles = vehicles.filter(vehicle_type=vehicle_type)

        if transmission:
            vehicles = vehicles.filter(transmission=transmission)

        if maximum_price is not None:
            vehicles = vehicles.filter(daily_price__lte=maximum_price)

    favorite_vehicles_ids = set()

    if request.user.is_authenticated:
        favorite_vehicles_ids = set(
            Favorite.objects.filter(user=request.user).values_list("vehicle_id", flat=True)
        )

    return render(
        request,
        "fleet/fleet_list.html",
        {
            "vehicles": vehicles,
            "form": form,
            "favorite_vehicles_ids": favorite_vehicles_ids,
        },
    )

def vehicle_detail(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    is_favorite = False

    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, vehicle=vehicle).exists()

    return render(
        request,
        "fleet/vehicle_detail.html",
        {
            "vehicle": vehicle,
            "is_favorite": is_favorite,
        },
    )

def route_list(request):
    routes = DrivingRoute.objects.prefetch_related("vehicles")

    return render(
        request,
        "fleet/route_list.html",
        {
            "routes": routes,
        },
    )

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related("vehicle")

    return render(
        request,
        "fleet/favorite_list.html",
        {
            "favorites": favorites,
        },
    )

@login_required
@require_POST
def toggle_favorite(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, vehicle=vehicle)

    if created:
        messages.success(request, f"{vehicle.name} has been added to your favorites.")
    else:
        favorite.delete()
        messages.success(request, f"{vehicle.name} has been removed from your favorites.")

    return redirect("fleet:vehicle_detail", vehicle_id=vehicle.id)
