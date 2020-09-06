from django.shortcuts import render
from rest_framework import generics, permissions, status
from .serializers import *
from core.models import VehicleTrip
from django_filters import rest_framework as filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework import status, permissions
import json


# Create your views here.
class CreateVehicleTripView(generics.CreateAPIView):
    """Create a new VehicleTrip in the system"""
    queryset = VehicleTrip.objects.all()
    serializer_class = VehicleTripSerializer
    permission_classes = [permissions.AllowAny]

# Update your views here.
class UpdateVehicleTripView(generics.UpdateAPIView):
    """Update a new VehicleTrip in the system"""
    queryset = VehicleTrip.objects.all()
    serializer_class = VehicleTripSerializer
    permission_classes = [permissions.AllowAny]

class VehicleTripFilter(filters.FilterSet):

    class Meta:
        model = VehicleTrip
        fields = {
            'starting_from': ['exact'], 
            'ending_at': ['exact'], 
            'starting_time': ['gt'],
            'tout': ['exact'],
            'vehicle': ['exact']
        }

class ListVehicleTripView(generics.ListAPIView):
    """Create a new VehicleTrip in the system"""
    queryset = VehicleTrip.objects.all()
    serializer_class = VehicleTripListSerializer
    permission_classes = [permissions.AllowAny]
    filter_fields = (
        'tout',
        'ending_at',
        'starting_time',
        'sacco'
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def getVehicleTrip(request):
    """Returns dashboard data based on requesting user"""
    vehicle = request.query_params['vehicle']
    print('vehicle', vehicle)

    try:
        trip = VehicleTrip.objects.filter(vehicle__regNo=vehicle).filter(ending_time=None).first()
        print('None time: ', trip.ending_time)
    except VehicleTrip.DoesNotExist:
        return  Response({'error': 'No Active Trip Found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = VehicleTripListSerializer(trip, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


class GetVehicleTripView(generics.RetrieveUpdateAPIView):
    """Create a new VehicleTrip in the system"""
    queryset = VehicleTrip.objects.all()
    serializer_class = VehicleTripListSerializer
    permission_classes = [permissions.AllowAny]

class GetSeatsByVehicleView(APIView):
    """Create a new user in the system"""
    # serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    def get_object(self, pk):
        result = VehicleTrip.objects.get(sacco=pk)
        # print(result)
        try:
            return VehicleTrip.objects.get(sacco=pk)
        except VehicleTrip.DoesNotExist:
            return  Response('Not Found', status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        seats = self.get_object(pk)
        serializer = VehicleTripListSerializer(seats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
