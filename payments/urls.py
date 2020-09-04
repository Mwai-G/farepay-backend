from . import views
from django.urls import path

app_name = 'payments'

urlpatterns = [
    path('', views.CreatePaymentsView.as_view(), name='list'),
    path('retrieve/<int:pk>', views.GetUpdatePaymentsView.as_view(), name='get/patch'),
]