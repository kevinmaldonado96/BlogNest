from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from .serializers import UserRegistrationSerializer
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer

from .models import User

class RegistrationUserView(APIView):
    permission_classes = [AllowAny]


    @extend_schema(
        summary="User registry",
        request=UserRegistrationSerializer,
        responses={
            201: UserRegistrationSerializer,
            400: OpenApiResponse(description="Bad request")            
}
    )
    def post(self, request):        
        
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user_response = serializer.save()
                        
            return Response(user_response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="User login",
        request=inline_serializer(
            name="LoginRequest",
            fields={
                "username": serializers.CharField(),
                "password": serializers.CharField()
            }
        ),
        responses={
            200: inline_serializer(
                name='Successfull response',
                fields={
                    "access": serializers.CharField(),
                    "refresh": serializers.CharField(),
                    "user": serializers.CharField()
                }
            ),
            404: OpenApiResponse(description="User not found or incorrect password")            
        }
    )
    def post(self, request):
        
        username = request.data.get("username")
        password = request.data.get("password")
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"detail": "User does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not check_password(password, user.password):
            return Response(
                {"detail": "Incorrect password."},
                status=status.HTTP_404_NOT_FOUND
            )
            
        token = RefreshToken.for_user(user)
            
        return Response({
            "access": str(token.access_token),
            "refresh": str(token),
            "user": user.username
        }, status=status.HTTP_200_OK)
            