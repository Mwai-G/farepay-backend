from . import views
from django.urls import path

app_name = 'routes'

urlpatterns = [
    path('list/', views.CreateRoutesView.as_view(), name='create/list'),
    path('retrieve/<int:pk>/', views.GetUpdateRoutesView.as_view(), name='get/put/patch'),

]