from django.urls import path

from . import views

app_name = "bookings"

urlpatterns = [
    path("create/<int:vehicle_id>/", views.create_booking, name="create_booking"),
    path("confirmation/<int:booking_id>/", views.booking_confirmation, name="confirmation"),
    path("my_bookings/", views.my_bookings, name="my_bookings"),
    path("cancel/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
    path("staff/", views.staff_dashboard, name="staff_dashboard"),
    path("review/<int:booking_id>/", views.review_booking, name="review_booking")
]
