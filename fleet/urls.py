from django.urls import path

from . import views

app_name = 'fleet'

urlpatterns = [
    path('', views.fleet_list, name='list'),
    path('routes/', views.routes_list, name='routes'),
    path('favorites/', views.favorites_list, name='favorites'),
    path('<int:pk>/', views.vehicle_detail, name='detail'),
    path('<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
]
