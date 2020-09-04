from django.shortcuts import render
from rest_framework import generics, permissions, status
from .serializers import *
from core.models import Vehicle, User

# Create your views here.
class CreateVehicleView(generics.ListCreateAPIView):
    """Create a new Vehicle in the system"""
    queryset = Vehicle.objects.all()
    serializer_class = VehiclePostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = (
        'sacco',
    )

# Create your views here.
class VehicleListView(generics.ListCreateAPIView):
    """Create a new Vehicle in the system"""
    queryset = Vehicle.objects.all()
    serializer_class = VehicleListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_fields = (
        'sacco',
        'driver', 'tout'
    )


class DetailVehicleView(generics.RetrieveDestroyAPIView):
    """Create a new Vehicle in the system"""
    queryset = Vehicle.objects.all()
    serializer_class = VehicleDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class UpdateVehicleView(generics.UpdateAPIView):
    """Create a new Vehicle in the system"""
    queryset = Vehicle.objects.all()
    serializer_class = VehiclePostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """
        If user role is tout or conductor,
        determines update of assigned_vehicle
        """
        # some actions
        user = request.user
        previous = self.get_object()
        update = request.data

        self.update_driver_records(previous, update)
        self.update_tout_records(previous, update)


        return super(UpdateVehicleView, self).update(request, *args, **kwargs) 

    def update_driver_records(self, previous, update):

        # when driver hasn't been posted and previous driver was none
        if (not update['driver'] and not previous.driver):
            return
        # when there is an change in driver
        if ((update['driver'] and not previous.driver) or (previous.driver.id != update['driver'])):

            # Unassign previous driver if existing
            if previous.driver is not None:
                prev_driver = User.objects.get(id=previous.driver.id)
                prev_driver.assigned_vehicle = False
                prev_driver.save()
            # Mark new driver as assigned
            if update['driver'] is not None:
                new_driver = User.objects.get(id=update['driver'])
                new_driver.assigned_vehicle = True
                new_driver.save()
        return

    def update_tout_records(self, previous, update):

        # when tout hasn't been posted and previous driver is none
        if (not update['tout'] and not previous.tout):
            return
        # when there is an change in tout
        if ((update['tout'] and not previous.tout) or (previous.tout.id != update['tout'])):

            # Unassign previous driver if existing
            if previous.tout is not None:
                prev_tout = User.objects.get(id=previous.tout.id)
                print('Prev tout: ', prev_tout)
                prev_tout.assigned_vehicle = False
                prev_tout.save()
            # Mark new tout as assigned
            if update['tout'] is not None:
                new_tout = User.objects.get(id=update['tout'])
                print('New tout: ', new_tout)
                new_tout.assigned_vehicle = True
                new_tout.save()
        return

