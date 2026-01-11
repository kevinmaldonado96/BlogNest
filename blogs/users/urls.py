from django.urls import path
from .views import RegistrationUserView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


urlpatterns = [
    path('register', RegistrationUserView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair")
]