from rest_framework import serializers
from core.models import Vehicle, User, Sacco, VehicleType, Routes
from user.serializers import UserSerializer
from sacco.serializers import SaccoSerializer
from routes.serializers import RoutesSerializer
from vehicletype.serializers import VehicleTypeSerializer

class VehiclePostSerializer(serializers.ModelSerializer):
    """Serializer for Vehicle while posting"""

    class Meta:
        model = Vehicle
        fields = '__all__'
        read_on_fields = ('id',)

class VehicleListSerializer(serializers.ModelSerializer):
    """Serializer for Vehicle objects"""
    owner = serializers.StringRelatedField()
    driver = serializers.StringRelatedField()
    tout = serializers.StringRelatedField()
    sacco = serializers.StringRelatedField()
    vehicleType = serializers.StringRelatedField()
    routes = serializers.StringRelatedField( )

    class Meta:
        model = Vehicle
        fields = ['id', 'regNo', 'tlb', 'created_at', 'owner', 'driver_id', 'driver', 'tout', 'tout_id', 'sacco', 'sacco_id', 'vehicleType', 'vehicleType_id', 'routes', 'routes_id']
        read_on_fields = ('id',)



class VehicleDetailSerializer(VehicleListSerializer):
    """Serializer for a Vehicle list view"""
    owner = UserSerializer(read_only=True)
    driver = UserSerializer(read_only=True)
    tout = UserSerializer(read_only=True)
    sacco = SaccoSerializer(read_only=True)
    routes = RoutesSerializer(read_only=True)
    vehicleType = VehicleTypeSerializer(read_only=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'regNo', 'tlb', 'created_at', 'owner', 'driver', 'tout', 'sacco', 'vehicleType', 'routes']
        read_on_fields = ('id',)