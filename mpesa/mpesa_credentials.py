import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64


class MpesaC2bCredential:
    consumer_key = 'je3S2L5H50xwUVWSnegyzeMs9ComiPjp'
    consumer_secret = 'ZeA9lllLwJAd3Rm9'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


class LipanaMpesaPpassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

    Business_short_code_1 = "174379"
    data_to_encode_1 = Business_short_code_1 + passkey + lipa_time
    online_password_1 = base64.b64encode(data_to_encode_1.encode())
    decode_password_1 = online_password_1.decode('utf-8')

    Business_short_code_2 = "174379"
    data_to_encode_2 = Business_short_code_2 + passkey + lipa_time
    online_password_2 = base64.b64encode(data_to_encode_2.encode())
    decode_password_2 = online_password_2.decode('utf-8')




class MpesaAccessToken:
    """Generates an mpesa_access_token"""
    r = requests.get(MpesaC2bCredential.api_URL,\
                     auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key,\
                     MpesaC2bCredential.consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']


def simulate_payment(shortcode, amount, acc_number):
    """Used to simulate mpesa C2B payment"""
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    headers = {"Authorization": "Bearer %s" % MpesaAccessToken.validated_mpesa_access_token}
    request = {"ShortCode": shortcode,
               "CommandID": "CustomerPayBillOnline",
               "Amount": amount,
               "Msisdn": '254708374149',
               "BillRefNumber": acc_number}
    response = requests.post(api_url, json=request, headers=headers)
    print(response.text)


