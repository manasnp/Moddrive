
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST

from .forms import RegistrationForm, EditProfileForm

from bookings.models import Booking
from fleet.models import Favorite


# Register a new user
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            customer_group = Group.objects.get(name="Customer")
            user.groups.add(customer_group)
            login(request, user)
            return redirect("home")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


# Login
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

    return render(
        request,
        "accounts/login.html",
        {"error_message": error_message}
    )


# Logout
@require_POST
def user_logout(request):
    logout(request)
    return redirect("home")


# Staff permissions
def is_booking_staff(user):
    return user.is_authenticated and user.has_perm(
        "bookings.change_booking"
    )


booking_staff_required = user_passes_test(is_booking_staff)


def is_fleet_manager(user):
    return user.is_authenticated and user.has_perm(
        "fleet.change_vehicle"
    )


fleet_manager_required = user_passes_test(is_fleet_manager)


# Profile page
@login_required
def profile(request):
    bookings = Booking.objects.filter(
        customer=request.user
    ).select_related("vehicle")

    context = {
        "total_bookings": bookings.count(),
        "pending_bookings": bookings.filter(status="pending").count(),
        "approved_bookings": bookings.filter(status="approved").count(),
        "favorite_count": Favorite.objects.filter(
            user=request.user
        ).count(),
        "recent_bookings": bookings[:5],
    }

    return render(request, "accounts/profile.html", context)


# Edit Profile page
@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            return redirect("accounts:profile")

    else:
        form = EditProfileForm(instance=request.user)

    return render(
        request,
        "accounts/edit_profile.html",
        {"form": form}
    )
