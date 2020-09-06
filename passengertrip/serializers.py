from rest_framework import serializers
from core.models import Vehicle, User, Sacco, VehicleTrip, Routes, PassengerTrip, Seats
from user.serializers import UserSerializer
from sacco.serializers import SaccoSerializer
from routes.serializers import RoutesSerializer
from vehicletrip.serializers import VehicleTripSerializer, VehicleTripListSerializer
from seats.serializers import SeatsSerializer



class PassengerTripSerializer(serializers.ModelSerializer):
    """Serializer for PassengerTrip objects"""

    class Meta:
        model = PassengerTrip
        fields = ['id', 'fare', 'pickup_at', 'created_at', 'drop_at', 'vehicleTrip', 'passenger', 'sacco', 'seat_no', 'confirmed']
        read_on_fields = ('id',)

class PassengerTripListSerializer(PassengerTripSerializer):
    """Serializer for PassengerTripList objects"""

    passenger = UserSerializer(read_only=True)
    sacco = SaccoSerializer(read_only=True)
    vehicleTrip = VehicleTripListSerializer(read_only=True)
    seatNo = SeatsSerializer(read_only=True)
    class Meta:
        model = PassengerTrip
        fields = '__all__'
        read_on_fields = ('id',)



