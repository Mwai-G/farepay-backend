from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ( 'password', 'phone','id','email', 'name', 'is_active', 'assigned_vehicle', 'role', 'sacco')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}, }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Adding custom fields
        token['name'] = user.name
        token['id'] = user.id
        token['role'] = user.role
        token['phone'] = user.phone

        try:
            token['saccoId'] = user.sacco.id
            token['sacco'] = user.sacco.name
        except Exception as exc:
            print('token error: ', exc)
            pass

        return token
