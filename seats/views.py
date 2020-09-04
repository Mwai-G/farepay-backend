from django.shortcuts import render
from rest_framework import generics, permissions, status
from .serializers import *
from core.models import Seats
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions

# Create your views here.
class CreateSeatsTripView(generics.ListCreateAPIView):
    """Create a new SeatsTrip in the system"""
    queryset = Seats.objects.all()
    serializer_class = SeatsSerializer
    permission_classes = [permissions.IsAuthenticated]

class GetUpdateSeatsTripView(generics.RetrieveUpdateAPIView):
    """Create a new SeatsTrip in the system"""
    queryset = Seats.objects.all()
    serializer_class = SeatsListSerializer
    permission_classes = [permissions.IsAuthenticated]

class GetSeatsByVehicleView(APIView):
    """Create a new user in the system"""
    # serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, pk):
        result = Seats.objects.get(vehicleTrip=pk)
        # print(result)
        try:
            return Seats.objects.get(vehicleTrip=pk)
        except Seats.DoesNotExist:
            return  Response('Not Found', status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        seats = self.get_object(pk)
        serializer = SeatsListSerializer(seats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
