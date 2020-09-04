from django.urls import path
from . import views


urlpatterns = [
    path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    path('online/lipa', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),

    path('callback-urls/register', views.register_urls, name="register_mpesa_validation"),
    path('validate', views.mpesa_validation, name="validation"),
    path('confirm', views.mpesa_confirmation, name="confirmation"),
]