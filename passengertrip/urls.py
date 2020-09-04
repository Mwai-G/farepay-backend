from . import views
from django.urls import path

app_name = 'passengertrip'

urlpatterns = [
    path('list/', views.ListPassengerTripView.as_view(), name='list_pax_trips'),
    path('retrieve/<int:pk>/', views.GetUpdatePassengerTripView.as_view(), name='get/put/patch'),
    path('create/', views.CreatePassengerTripView.as_view(), name='create_pax_trip'),
    path('get/', views.GetPassengerTripView.as_view(), name='get trip by pNo')
]