from django.shortcuts import render
from rest_framework import generics, permissions, status
from .serializers import *
from core.models import Sacco

# Create your views here.
class CreateSaccoView(generics.ListCreateAPIView):
    """Create a new Sacco in the system"""
    queryset = Sacco.objects.all()
    serializer_class = SaccoSerializer
    permission_classes = [permissions.IsAuthenticated]

class GetUpdateSaccoView(generics.RetrieveUpdateAPIView):
    """Create a new Sacco in the system"""
    queryset = Sacco.objects.all()
    serializer_class = SaccoSerializer
    permission_classes = [permissions.IsAuthenticated]