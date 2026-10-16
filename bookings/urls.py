from django.urls import path

from . import views

app_name = 'bookings'

urlpatterns = [
    path('mine/', views.my_bookings, name='mine'),
    path('create/<int:vehicle_id>/', views.create_booking, name='create'),
    path('<int:pk>/confirmation/', views.booking_confirmation, name='confirmation'),
    path('<int:pk>/cancel/', views.cancel_booking, name='cancel'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/<int:pk>/review/', views.review_booking, name='review'),
]
