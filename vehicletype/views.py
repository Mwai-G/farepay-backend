from django.shortcuts import render
from rest_framework import generics, permissions, status
from .serializers import *
from core.models import VehicleType

# Create your views here.
class CreateVehicleTypeView(generics.ListCreateAPIView):
    """Create a new VehicleType in the system"""
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class GetUpdateVehicleTypeView(generics.RetrieveUpdateDestroyAPIView):
    """Create a new VehicleType in the system"""
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    permission_classes = [permissions.IsAuthenticated]