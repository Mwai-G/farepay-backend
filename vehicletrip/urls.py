from . import views
from django.urls import path

app_name = 'vehicletrip'

urlpatterns = [
    path('create/', views.CreateVehicleTripView.as_view(), name='create'),
    path('list/', views.ListVehicleTripView.as_view(), name='list'),
    path('vehicle/', views.getVehicleTrip),
    path('retrieve/<int:pk>/', views.GetVehicleTripView.as_view(), name='get/put/patch'),
    path('update/<int:pk>/', views.UpdateVehicleTripView.as_view(), name='get/put/patch'),
    path('sacco/<int:pk>/', views.GetSeatsByVehicleView.as_view(), name='patch')
]