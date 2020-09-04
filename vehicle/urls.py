from . import views
from django.urls import path

app_name = 'vehicle'

urlpatterns = [
    path('create/', views.CreateVehicleView.as_view(), name='create'),
    path('list/', views.VehicleListView.as_view(), name='list'),
    path('retrieve/<int:pk>/', views.DetailVehicleView.as_view(), name='get_vehicle_detail'),
    path('update/<int:pk>/', views.UpdateVehicleView.as_view(), name='edit_vehicle')
]