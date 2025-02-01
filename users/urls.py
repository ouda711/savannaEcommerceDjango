from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import Register

app_name = 'users'

urlpatterns = [
    path('users/', Register.as_view(), name="register"),
    path('users/register', Register.as_view(), name="register"),
    path('users/login', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('auth/login', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('auth/token/refresh', TokenRefreshView.as_view(), name="token_refresh"),
]
