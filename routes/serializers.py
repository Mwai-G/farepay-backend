from rest_framework import serializers
from core.models import Routes


class RoutesSerializer(serializers.ModelSerializer):
    """Serializer for Routes objects"""

    class Meta:
        model = Routes
        fields = ['id', 'starting_from', 'ending_at', 'sacco', 'minRate', 'maxRate', 'created_at', 'updated_at']
        read_on_fields = ('id',)