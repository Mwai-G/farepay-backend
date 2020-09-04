from . import views
from django.urls import path

app_name = 'vehicletype'

urlpatterns = [
    path('list/', views.CreateVehicleTypeView.as_view(), name='create/list'),
    path('retrieve/<int:pk>/', views.GetUpdateVehicleTypeView.as_view(), name='get/put/patch'),

]