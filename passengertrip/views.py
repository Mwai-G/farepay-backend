from django.shortcuts import render
from rest_framework import generics, permissions, status
from .serializers import *
from core.models import PassengerTrip

# Create your views here.
class CreatePassengerTripView(generics.ListCreateAPIView):
    """Create a new PassengerTrip in the system"""
    queryset = PassengerTrip.objects.all()
    serializer_class = PassengerTripSerializer
    permission_classes = [permissions.IsAuthenticated]

class GetUpdatePassengerTripView(generics.RetrieveUpdateAPIView):
    """Create a new PassengerTrip in the system"""
    queryset = PassengerTrip.objects.all()
    serializer_class = PassengerTripListSerializer
    permission_classes = [permissions.AllowAny]

class ListPassengerTripView(generics.ListAPIView):
    """List PassengerTrips in the system"""
    queryset = PassengerTrip.objects.all()
    serializer_class = PassengerTripListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = (
        'passenger_name',
        'passenger_phone',
        'sacco'
        )

class GetPassengerTripView(generics.ListAPIView):
    """List PassengerTrips in the system"""
    queryset = PassengerTrip.objects.all()
    serializer_class = PassengerTripListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = (
        'passenger_phone',
        )


