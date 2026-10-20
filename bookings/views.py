from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from accounts.views import booking_staff_required
from bookings.forms import BookingForm, BookingDecisionForm
from fleet.models import Vehicle
from .models import Booking

@login_required
def create_booking(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, is_available=True)

    if request.method == "POST":
        form = BookingForm(request.POST, vehicle=vehicle)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.vehicle = vehicle
            rental_days = (booking.end_date - booking.start_date).days + 1
            booking.total_price = rental_days * vehicle.daily_price

            if booking.route:
                booking.total_price += booking.route.additional_price

            try:
                booking.save()
            except ValidationError as error:
                form.add_error(None, error)
            else:
                messages.success(request, "Your booking request has been submitted successfully.")

                return redirect("bookings:confirmation", booking_id=booking.id)
         
    else:
        form = BookingForm(vehicle=vehicle)

    return render(request, "bookings/booking_form.html", {"form": form, "vehicle": vehicle})

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)

    return render(request, "bookings/booking_confirmation.html", {"booking": booking})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(customer=request.user).select_related("vehicle", "route").order_by("-created_at")

    return render(request, "bookings/my_bookings.html", {"bookings": bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user, status="pending")

    if request.method == "POST":
        booking.status = "cancelled"
        booking.save()
        messages.success(request, "Your booking has been cancelled.")

    return redirect("bookings:my_bookings")

@booking_staff_required
def staff_dashboard(request):
    bookings = Booking.objects.select_related(
        "customer", "vehicle", "route"
    ).order_by("-created_at")

    pending_bookings = bookings.filter(status="pending")

    return render(request, "bookings/staff_dashboard.html", {
        "bookings": bookings,
        "pending_bookings": pending_bookings,
        "pending_count": pending_bookings.count(),
        "approved_count": bookings.filter(status="approved").count(),
        "denied_count": bookings.filter(status="denied").count(),
    })
@booking_staff_required
def review_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        status__in=["pending", "approved", "denied"]
    )
    if request.method == "POST":
        form = BookingDecisionForm(request.POST, instance=booking)
        if form.is_valid():
            try:
                form.save()
            except ValidationError as error:
                form.add_error(None, error)
            else:
                messages.success(request, "Booking status has been updated successfully.")
                return redirect("bookings:staff_dashboard")
    else:
        form = BookingDecisionForm(instance=booking)

    return render(request, "bookings/review_booking.html", {"form": form, "booking": booking})
