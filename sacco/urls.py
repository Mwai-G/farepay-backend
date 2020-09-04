from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

app_name = 'sacco'

urlpatterns = [
    path('list/', CreateSaccoView.as_view(), name='create/list'),
    path('retrieve/<int:pk>/', GetUpdateSaccoView.as_view(), name='get/put/patch')
]
