from rest_framework import serializers
from user.serializers import UserSerializer
from routes.serializers import RoutesSerializer
from vehicletype.serializers import VehicleTypeSerializer
from core.models import Sacco,Seats,Vehicle,VehicleTrip,VehicleType,PassengerTrip,PaymentMethod,Routes,User

class SaccoSerializer(serializers.ModelSerializer):
    """Serializer for Sacco objects"""

    class Meta:
        model = Sacco
        fields = ['id', 'name', 'address', 'email', 'phone', 'created_at']
        read_on_fields = ('id',)






