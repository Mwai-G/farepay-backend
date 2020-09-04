from rest_framework import serializers
from core.models import Vehicle, User, Sacco, Vehicle, Routes, VehicleTrip
from user.serializers import UserSerializer
from sacco.serializers import SaccoSerializer
from routes.serializers import RoutesSerializer
from vehicle.serializers import VehicleListSerializer

class VehicleTripSerializer(serializers.ModelSerializer):
    """Serializer for Vehicle while posting"""

    class Meta:
        model = VehicleTrip
        fields = '__all__'
        read_on_fields = ('id',)


class VehicleTripListSerializer(VehicleTripSerializer):
    """Serializer for VehicleTripList objects"""
    driver = UserSerializer()
    tout = UserSerializer()
    sacco = SaccoSerializer()
    vehicle = VehicleListSerializer()

    class Meta:
        model = VehicleTrip
        fields = ['id', 'starting_from', 'ending_at', 'created_at', 'max_rate', 'min_rate', 'starting_time', 'ending_time', 'driver', 'tout', 'sacco', 'vehicle','price']
        read_on_fields = ('id',)