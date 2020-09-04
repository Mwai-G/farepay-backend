from rest_framework import serializers
from core.models import VehicleType

class VehicleTypeSerializer(serializers.ModelSerializer):
    """Serializer for VehicleType objects"""

    class Meta:
        model = VehicleType
        fields = ['id', 'name', 'seats_no', 'driver_seat_no', 'tout_seat_no', 'created_at']
        read_on_fields = ('id',)