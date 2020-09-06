from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView
from . import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateSaccoUserView.as_view(), name='create'),
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('list/', views.UserViewList.as_view(), name='user_list'),
    path('token/', views.CustomJWTPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('detail/', views.ManageUserView.as_view(), name='user_detail'),
    path('detail/<int:pk>/', views.RetrieveUserView.as_view(), name='user_detail_id'),
    path('deactivate/<int:pk>/', views.DeactivateUserView.as_view(), name='user_deactivate_id'),
]
