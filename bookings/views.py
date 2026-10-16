from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from fleet.models import Vehicle
from .forms import BookingDecisionForm, BookingForm
from .models import Booking


@login_required
def create_booking(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id, is_available=True)
    if request.method == 'POST':
        form = BookingForm(request.POST, vehicle=vehicle)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.vehicle = vehicle
            try:
                booking.save()
            except Exception as exc:
                form.add_error(None, str(exc))
            else:
                messages.success(request, 'Your booking request was submitted for staff review.')
                return redirect('bookings:confirmation', pk=booking.pk)
    else:
        form = BookingForm(vehicle=vehicle)
    return render(request, 'bookings/booking_form.html', {'form': form, 'vehicle': vehicle})


@login_required
def booking_confirmation(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)
    return render(request, 'bookings/booking_confirmation.html', {'booking': booking})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(customer=request.user).select_related('vehicle', 'route')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.user, status='pending')
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save(update_fields=['status', 'estimated_price', 'updated_at'])
        messages.info(request, 'The booking request was cancelled.')
    return redirect('bookings:mine')


def is_booking_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@user_passes_test(is_booking_staff)
def staff_dashboard(request):
    bookings = Booking.objects.select_related('customer', 'vehicle', 'route')
    return render(request, 'bookings/staff_dashboard.html', {
        'bookings': bookings,
        'pending_count': bookings.filter(status='pending').count(),
        'approved_count': bookings.filter(status='approved').count(),
        'vehicle_count': Vehicle.objects.count(),
    })


@user_passes_test(is_booking_staff)
def review_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingDecisionForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, f'Booking #{booking.pk} was updated.')
            return redirect('bookings:staff_dashboard')
    else:
        form = BookingDecisionForm(instance=booking)
    return render(request, 'bookings/booking_review.html', {'booking': booking, 'form': form})
