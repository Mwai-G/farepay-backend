from rest_framework import serializers
from core.models import Vehicle, User, Sacco, VehicleTrip, Routes, PassengerTrip, Seats
from user.serializers import UserSerializer
from sacco.serializers import SaccoSerializer
from routes.serializers import RoutesSerializer
from vehicletrip.serializers import VehicleTripSerializer


class SeatsSerializer(serializers.ModelSerializer):
    """Serializer for Seats objects"""
    class Meta:
        model = Seats
        fields = ['id', 'seatNo', 'occStatus', 'created_at', 'payStatus', 'vehicleTrip']
        read_on_fields = ('id',)

class SeatsListSerializer(serializers.ModelSerializer):
    """Serializer for SeatsList objects"""

    vehicleTrip = VehicleTripSerializer(read_only=True)

    class Meta:
        model = Seats
        fields = ['id', 'seatNo', 'occStatus', 'created_at', 'payStatus', 'vehicleTrip']
        read_on_fields = ('id',)