from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from .forms import RegistrationForm
from django.contrib.auth.decorators import user_passes_test

# Create your account views here.
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            customer_group = Group.objects.get(name="Customer")
            user.groups.add(customer_group)
            login(request,user)
            return redirect("home")  # Redirect to the home page after successful registration
    else:
        form = RegistrationForm()
    
    return render(request, "accounts/register.html", {"form": form})

def user_login(request):
    error_message = None
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")

        else:
            error_message = "Invalid email or password."

    return render(request, "accounts/login.html", {"error_message": error_message})

@require_POST
def user_logout(request):
    logout(request)
    return redirect("home")           

def is_booking_staff(user):
    return user.is_authenticated and user.has_perm("bookings.change_booking")
booking_staff_required = user_passes_test(is_booking_staff)

def is_fleet_manager(user):
    return user.is_authenticated and user.has_perm("fleet.change_vehicle")
fleet_manager_required = user_passes_test(is_fleet_manager) 