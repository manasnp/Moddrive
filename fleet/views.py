from django.shortcuts import render


# Create your fleet views here.
from django.shortcuts import render
from .models import Vehicle


def vehicle_list(request):
    vehicles = Vehicle.objects.all()

    return render(
        request,
        "fleet/fleet_list.html",
        {"vehicles": vehicles},
    )