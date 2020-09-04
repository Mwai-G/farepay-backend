from rest_framework import serializers
from core.models import Payment
from user.serializers import UserSerializer
from passengertrip.serializers import PassengerTripSerializer
from vehicletrip.serializers import VehicleTripSerializer
from sacco.serializers import SaccoSerializer
from seats.serializers import SeatsListSerializer

class PaymentListSerializer(serializers.ModelSerializer):
    """Serializer for VehicleTripList objects"""
    passenger = UserSerializer()
    # method = UserSerializer()
    passTrip = PassengerTripSerializer()
    vehicleTrip = VehicleTripSerializer()
    sacco =  SaccoSerializer()

    class Meta:
        model = Payment
        fields = '__all__'
        # read_on_fields = ('id',)