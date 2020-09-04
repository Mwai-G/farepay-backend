
import uuid
import os
import phonenumbers

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings
from django.utils.translation import gettext as _


class BaseModel(models.Model):
    """
    Used to track at what time a record was recorded in the database without repetition
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True


#Django model utils TimeStampedModel
class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        """Creates and saves a new user"""
        print(extra_fields)
        if not phone:
            raise ValueError('Users must have an phone number')
        if not password:
            raise ValueError('Users must have a password')
        try:
            extra_fields['role']
        except Exception:
            raise ValueError('Users must have a role')
        try:
            extra_fields['name']
        except Exception:
            raise ValueError('Users must have a name')           
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password):
        """Creates and saves a new super user"""
        user = self.model(phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    ROLES = (
       ('Sacco Admin', _('Sacco Admin')),
       ('Owner', _('Owner')),
       ('Tout', _('Tout')),
       ('Driver', _('Driver')),
       ('Passenger', _('Passenger')),
       ('MOH', _('MOH')),
       ('NTSA', _('NTSA')),
       ('KRA', _('KRA')),
       ('INTERIOR', _('INTERIOR')),
   )


    """Custom user model that supports using phone instead of username"""
    phone = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False, null=True)
    # used for drivers and touts only
    assigned_vehicle = models.BooleanField(default=False)
    role = models.CharField(
       max_length=32,
       choices=ROLES,
       default='Sacco Admin'
    )
    sacco = models.ForeignKey(
        'Sacco',
        on_delete=models.CASCADE,
        related_name='user_sacco',
        blank=True, null=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'phone'

    def formatted_phone(self, country=None):
        return phonenumbers.parse(self.phone, country)

    def __str__(self):
        return self.name


class Sacco(models.Model):
    """Sacco for vehicles"""
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    paybill = models.CharField(max_length=255, unique=True, null=True)


    def __str__(self):
        return self.name

class Routes(TimeStampMixin):
    """Routes for vehicles"""
    starting_from = models.CharField(max_length=255)
    ending_at = models.CharField(max_length=255)
    sacco = models.ForeignKey(
        'Sacco',
        on_delete=models.CASCADE,
        related_name='routes_sacco'
    )
    minRate = models.CharField(max_length=255)
    maxRate = models.CharField(max_length=255)
    # created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.starting_from + ' -> ' + self.ending_at      


class VehicleType(models.Model):
    """VehicleType for vehicles"""
    name = models.CharField(max_length=255)
    seats_no = models.CharField(max_length=255)
    driver_seat_no = models.CharField(max_length=255)
    tout_seat_no = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    """Vehicles registered"""
    regNo = models.CharField(max_length=255)
    tlb = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        related_name='owner'
    )
    driver = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        related_name='driver'
    )
    tout = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        related_name='tout'
    )
    sacco = models.ForeignKey(
        'Sacco',
        on_delete=models.CASCADE,
        related_name='sacco'
    )
    vehicleType = models.ForeignKey(
        'VehicleType',
        null=True,
        on_delete=models.CASCADE,
        related_name='vehicle_type'
    )
    routes = models.ForeignKey(
        'Routes',
        null=True,
        on_delete=models.CASCADE,
        related_name='routes'
    )

    def __str__(self):
        return self.regNo


class VehicleTrip(models.Model):
    """Trips taken by a vehicle"""
    created_at = models.DateTimeField(auto_now=True)
    starting_from = models.CharField(max_length=255)
    ending_at = models.CharField(max_length=255)
    max_rate = models.CharField(max_length=255, default=0)
    min_rate = models.CharField(max_length=255, default=0)
    price = models.CharField(max_length=255, default=0)
    starting_time = models.DateTimeField()
    ending_time = models.DateTimeField(null=True, blank=True)
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vehicle_trip_driver'
    )
    tout = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vehicle_trip_tout'
    )
    sacco = models.ForeignKey(
        'Sacco',
        on_delete=models.CASCADE,
        related_name='vehicle_trip_sacco'
    )
    vehicle = models.ForeignKey(
        'Vehicle',
        on_delete=models.CASCADE,
        related_name='vehicle_trip'
    )

    # def __str__(self):
        # return self.starting_from + '('+ self.starting_time + ')' + '->' + self.ending_at + '('+ self.ending_time + ')'

class PassengerTrip(models.Model):
    PAYMENT_METHODS = (
       ('Cash', _('Cash')),
       ('Mpesa', _('Mpesa')),
       ('PesaLink', _('PesaLink')),
   )
    """Trips taken by a passenger"""
    created_at = models.DateTimeField(auto_now=True)
    pickup_at = models.CharField(max_length=255, null=True)
    drop_at = models.CharField(max_length=255, null=True)
    confirmed = models.BooleanField(default=False, null=True)
    passenger_name = models.CharField(max_length=255, default='Anonymous')
    passenger_phone = models.CharField(max_length=255, default='Not recorded')
    fare = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255, choices=PAYMENT_METHODS, default='Mpesa')
    seat_no = models.IntegerField(default=0)
    vehicleTrip = models.ForeignKey(
        'VehicleTrip',
        on_delete=models.CASCADE,
        related_name='passenger_vehicle_trip'
    )
    passenger = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='passenger_trip_user',
        null=True  # incase user isn't logged in
    )
    sacco = models.ForeignKey(
        'Sacco',
        on_delete=models.CASCADE,
        related_name='passenger_trip_sacco'
    )

    def __str__(self):
        return str(self.id)


class PaymentMethod(models.Model):
    """Available methods of payment"""
    created_at = models.DateTimeField(auto_now=True)
    method = models.CharField(max_length=255)

    def __str__(self):
        return self.method


class Payment(models.Model):
    """payments made"""
    created_at = models.DateTimeField(auto_now=True)
    amount = models.CharField(max_length=255)
    passenger_name = models.CharField(max_length=255)
    passenger_phone = models.CharField(max_length=255)
    passenger = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='passenger_trip_payment_user',
        null=True  # incase user isn't logged in
    )
    method = models.CharField(max_length=255)
    passTrip = models.ForeignKey(
        'PassengerTrip',
        on_delete=models.CASCADE,
        related_name='passenger_trip_payment'
    )
    vehicleTrip = models.ForeignKey(
        'VehicleTrip',
        on_delete=models.CASCADE,
        related_name='vehicle_trip_payment'
    )
    sacco = models.ForeignKey(
        'Sacco',
        on_delete=models.CASCADE,
        related_name='passenger_trip_sacco_payment'
    )
    seatNo = models.CharField(max_length=255)

    def __str__(self):
        return self.amount


class MpesaPayment(BaseModel):
    """
    Used to store successful mpesa transactions.
    """
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    transaction_id = models.CharField(max_length=225, default="")
    transaction_type = models.CharField(max_length=225, default="")
    paybill_no = models.CharField(max_length=225, default="") 
    reference = models.CharField(max_length=225)
    first_name = models.CharField(max_length=225)
    middle_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    phone_number = models.CharField(max_length=225)
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)


class Seats(models.Model):
    """seats in a vehicle trip"""
    created_at = models.DateTimeField(auto_now=True)
    seatNo = models.CharField(max_length=255)
    occStatus = models.BooleanField(default=False)
    payStatus = models.BooleanField(default=False)
    vehicleTrip = models.ForeignKey(
        'VehicleTrip',
        on_delete=models.CASCADE,
        related_name='vehicle_trip_seat'
    )

    def __str__(self):
        return self.seatNo

class Wallet(models.Model):
    """wallet for making payments"""
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField()
    amount = models.CharField(max_length=255)
    passenger = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='app_user_wallet'
    )

    def __str__(self):
        return self.amount

