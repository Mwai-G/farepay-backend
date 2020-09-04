from django.shortcuts import render
from rest_framework import generics, permissions, status
from .serializers import *
from core.models import Payment

# Create your views here.
class CreatePaymentsView(generics.ListCreateAPIView):
    """Create a new Payments in the system"""
    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer
    permission_classes = [permissions.IsAuthenticated]

class GetUpdatePaymentsView(generics.RetrieveUpdateAPIView):
    """Create a new Payments in the system"""
    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer
    permission_classes = [permissions.IsAuthenticated]