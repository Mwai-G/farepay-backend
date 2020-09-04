import json
import requests
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword, MpesaC2bCredential, simulate_payment
from core import models
from rest_framework.response import Response
from rest_framework.views import status


def getAccessToken(request):
    consumer_key = MpesaC2bCredential.consumer_key
    consumer_secret = MpesaC2bCredential.consumer_secret
    api_URL = MpesaC2bCredential.api_URL
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)

@api_view(['POST'])
@permission_classes([AllowAny])
def lipa_na_mpesa_online(request):
    data = request.data  # phone, vehicleReg, account_no
    print('Data is: ', data)
    regNo = data['vehicleReg']
    vTrip = models.VehicleTrip.objects.filter(vehicle__regNo=regNo).first()
    sacco = vTrip.sacco
    amt = 1
    seatNo=data['seatNo']
    phone = data['phone']
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code_2,
        "Password": LipanaMpesaPpassword.decode_password_2,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amt,
        "PartyA": phone,
        "PartyB": LipanaMpesaPpassword.Business_short_code_2,
        "PhoneNumber": phone,
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": f"{sacco}-{regNo}-S{data['seatNo']}",
        "TransactionDesc": f"Fare payment for bus {regNo} of {amt}"
    }
    response = requests.post(api_url, json=request, headers=headers)
    print(vTrip.starting_from)
  
    sacco = vTrip.sacco
    phone = '0' + phone[slice(3, 13)]
    print(phone)
    try:
        passenger = models.User.objects.get(phone=phone)
        passenger_name=passenger.name
    except models.User.DoesNotExist:
        passenger=None
        passenger_name='Anonymous'
    print(passenger_name)
    passenger_trip = models.PassengerTrip.objects.create(
        pickup_at=vTrip.starting_from,
        drop_at=vTrip.ending_at,
        confirmed=True,
        passenger_name=passenger_name,
        passenger_phone=phone,
        fare=vTrip.price,
        seat_no=seatNo,
        vehicleTrip=vTrip,
        passenger=passenger,
        sacco=sacco
    )

    payment = models.Payment.objects.create(
        passenger_name=passenger_name,
        passenger_phone=phone,
        amount=vTrip.price,
        passenger=passenger,
        method='MPESA',
        passTrip=passenger_trip,
        vehicleTrip=vTrip,
        seatNo=seatNo,
        sacco=sacco
    )
    print(passenger_trip)
    return Response({'message': passenger_trip.id}, status=status.HTTP_200_OK)



@csrf_exempt
@permission_classes([AllowAny])
def register_urls(request):
    """
    Method used to register confirmation and validation URL with Safaricom.
    """
    access_token = MpesaAccessToken.validated_mpesa_access_token
    print(access_token)
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Business_short_code_1,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://746501842e36.ngrok.io/api/mobile-money/confirm",
               "ValidationURL": "https://746501842e36.ngrok.io/api/mobile-money/validate"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)


@csrf_exempt
@permission_classes([AllowAny])
def mpesa_validation(request):
    """
    Method used to accept the payment by responding with ResultCode: 0 and ResultDesc: Accepted. 
    If ResultCode changed from 0 to any other number, you reject the payment.
    Returns json format since Mpesa expects json format.
    """
    print('_____________VALIDATION URL HAS BEEN HIT____________________')
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


@csrf_exempt
@permission_classes([AllowAny])
def mpesa_confirmation(request):
    """
    A function used to save successfully transaction in our database.
    The mpesa transaction is attained from the body by decoding using utf-8
    """
    print('_____________CONFIRMATION URL HAS BEEN HIT____________________')
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)  # access of variables in our request.

    # Get payment's associated user, property & unit
    # associations = get_associations(mpesa_payment['BusinessShortCode'],\
    #                                 mpesa_payment['BillRefNumber'], 'Mpesa')
    # Save payment to MPESA model
    pay = models.MpesaPayment.objects.create(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        transaction_id=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        paybill_no=mpesa_payment['BusinessShortCode'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        transaction_type=mpesa_payment['TransactionType'],
    )



    amount = pay.amount
    phone = f"0{pay.phone_number[slice(3, -1)]}"
    name = f"{pay.first_name} {pay.middle_name} {pay.last_name}"
    payment_method = 'Mpesa'

    # kaa123q-2
    details = pay.reference.split('-')
    seat_no = details[-1]

    rn = f"{details[0][slice(0,3)]} {details[0][slice(3,7)]}"
    reg_no = rn.upper()
    vehicle_trip = models.VehicleTrip.objects.filter(vehicle__regNo=reg_no).latest('created_at')

    sacco = vehicle_trip.sacco

    try:
        passenger = models.User.objects.get(phone=phone)
    except models.User.DoesNotExist:
        passenger = None


    passenger_trip = models.PassengerTrip.objects.create(
        passenger_name=name,
        passenger_phone=phone,
        fare=amount,
        payment_method=payment_method,
        seat_no=seat_no,
        vehicleTrip=vehicle_trip,
        passenger=passenger,
        sacco=sacco
    )


    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    print(f'{pay.first_name} has made payment of {pay.amount}')
    return JsonResponse(dict(context))



@csrf_exempt
@permission_classes([AllowAny])
def simulateC2BTrigger(request):
    """
    Method used to register confirmation and validation URL with Safaricom.
    """
    data = request.data
    try:
        simulate_payment(data['shortcode'], data['amt'], data['acc_no'])
    except Exception as exc:
        print('Simulation of C2B failed with error: ', exc)
