from django.shortcuts import render
from rest_framework import generics, permissions, status
from .serializers import *
from core.models import Routes

# Create your views here.
class CreateRoutesView(generics.ListCreateAPIView):
    """Create a new Routes in the system"""
    queryset = Routes.objects.all()
    serializer_class = RoutesSerializer
    permission_classes = [permissions.IsAuthenticated]

class GetUpdateRoutesView(generics.RetrieveUpdateAPIView):
    """Create a new Routes in the system"""
    queryset = Routes.objects.all()
    serializer_class = RoutesSerializer
    permission_classes = [permissions.IsAuthenticated]