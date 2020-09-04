from . import views
from django.urls import path

app_name = 'seats'

urlpatterns = [
    path('list/', views.CreateSeatsTripView.as_view(), name='create/list'),
    path('retrieve/<int:pk>/', views.GetUpdateSeatsTripView.as_view(), name='get/put/patch'),
    path('vehicletrip/<int:pk>/', views.GetSeatsByVehicleView.as_view(), name='get by vehicle')
]