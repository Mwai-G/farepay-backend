from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions, status
from rest_framework.settings import api_settings
from .serializers import UserSerializer, AuthTokenPairSerializer
from rest_framework.response import Response
from core.models import User, Sacco
from sacco.serializers import SaccoSerializer
from rest_framework.views import APIView

class CreateSaccoUserView(APIView):
    """Create a new user in the system"""
    # serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        """Post(sacco, user)"""
        # print(request.data)
        user_serializer = UserSerializer(data=request.data['user'])
        sacco_serializer = SaccoSerializer(data=request.data['sacco'])
        user_is_valid = user_serializer.is_valid(raise_exception = True)
        sacco_is_valid = sacco_serializer.is_valid(raise_exception = True)

        errors = {}
        if sacco_is_valid and user_is_valid:
            sacco = sacco_serializer.save()
            request.data['user']['sacco'] = sacco.id
            user_serializer = UserSerializer(data=request.data['user'])
            user_serializer.is_valid()
            user_serializer.save()
            return Response({'sacco': sacco_serializer.data,
                             'user': user_serializer.data},
                              status=status.HTTP_201_CREATED)
        elif not user_serializer.is_valid():
            error['sacco'] = sacco_serializer.errors
        elif not user_serializer.is_valid():
            error['user'] = user_serializer.errors
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)          


class CreateUserView(generics.ListCreateAPIView):
    """Create a new user in the system"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    filter_fields = (
        'sacco',
        'role',
        )


class UserViewList(generics.ListAPIView):
    """List PassengerTrips in the system"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    filter_fields = (
        'sacco',
        'role',
        )


class CustomJWTPairView(TokenObtainPairView):
    serializer_class = AuthTokenPairSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user

class RetrieveUserView(generics.RetrieveUpdateAPIView):
    """Retrieve the authenticated user"""
    serializer_class = UserSerializer

    def get_object(self, pk):
        """Retrieve and return user by ID"""
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Http404
    
    def get(self, request,  pk, format=None):
        """get a restaurant menu Category by id"""

        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeactivateUserView(generics.RetrieveUpdateAPIView):
    """Deactivate the authenticated user"""
    serializer_class = UserSerializer

    def get_object(self, pk):
        """Deactivate and return user by ID"""
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Http404
    
    def delete(self, request,  pk, format=None):
        """get a restaurant menu Category by id"""

        user = self.get_object(pk)
        user.is_active = False
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
