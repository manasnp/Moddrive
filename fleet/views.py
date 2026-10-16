from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import DrivingRoute, Favorite, Vehicle


def home(request):
    featured = Vehicle.objects.filter(is_available=True, is_featured=True)[:3]
    if not featured:
        featured = Vehicle.objects.filter(is_available=True)[:3]
    return render(request, 'home.html', {'featured_vehicles': featured})


def fleet_list(request):
    vehicles = Vehicle.objects.filter(is_available=True)
    query = request.GET.get('q', '').strip()
    vehicle_type = request.GET.get('type', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    if query:
        vehicles = vehicles.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if vehicle_type:
        vehicles = vehicles.filter(vehicle_type=vehicle_type)
    if max_price:
        try:
            vehicles = vehicles.filter(daily_price__lte=max_price)
        except ValueError:
            pass

    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(Favorite.objects.filter(user=request.user).values_list('vehicle_id', flat=True))

    return render(request, 'fleet/fleet_list.html', {
        'vehicles': vehicles,
        'vehicle_types': Vehicle.TYPE_CHOICES,
        'favorite_ids': favorite_ids,
    })


def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    is_favorite = request.user.is_authenticated and Favorite.objects.filter(
        user=request.user, vehicle=vehicle
    ).exists()
    return render(request, 'fleet/vehicle_detail.html', {
        'vehicle': vehicle,
        'is_favorite': is_favorite,
    })


def routes_list(request):
    return render(request, 'fleet/routes.html', {'routes': DrivingRoute.objects.all()})


@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('vehicle')
    return render(request, 'fleet/favorites.html', {'favorites': favorites})


@login_required
def toggle_favorite(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, vehicle=vehicle)
    if not created:
        favorite.delete()
        messages.info(request, f'{vehicle.name} was removed from Favorites.')
    else:
        messages.success(request, f'{vehicle.name} was saved to Favorites.')
    return redirect(request.POST.get('next') or 'fleet:detail', pk=vehicle.pk)
