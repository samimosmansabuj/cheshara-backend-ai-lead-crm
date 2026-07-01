from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from .choices import OTPPurpose
from .models import OTPVerification, User
from .serializers import (
    AdminLoginSerializer,
    ClientSendOTPSerializer,
    ClientVerifyOTPSerializer,
)


class ClientSendOTPAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ClientSendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone_number"].strip()
        user, _ = User.objects.get_or_create(phone_number=phone)
        OTPVerification.objects.create_otp(
            user=user,
            phone_number=phone,
            purpose=OTPPurpose.LOGIN,
        )

        # TODO: Send OTP via Twilio

        return Response(
            {
                "success": True,
                "message": "OTP sent successfully.",
                "data": None,
            },
            status=status.HTTP_200_OK,
        )

class ClientVerifyOTPAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ClientVerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(
            {
                "success": True,
                "message": "Login successful.",
                "data": {
                    "access": result["access"],
                    "refresh": result["refresh"],
                    "user": {
                        "id": result["user"].id,
                        "phone_number": result["user"].phone_number,
                        "full_name": result["user"].full_name,
                        "user_type": result["user"].user_type,
                        "is_phone_verified": result["user"].is_phone_verified,
                    },
                },
            },
            status=status.HTTP_200_OK,
        )

class AdminLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return Response(
            {
                "success": True,
                "message": "Login successful.",
                "data": {
                    "access": serializer.validated_data["access"],
                    "refresh": serializer.validated_data["refresh"],
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "phone_number": user.phone_number,
                        "full_name": user.full_name,
                        "user_type": user.user_type,
                    },
                },
            },
            status=status.HTTP_200_OK,
        )

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "success": True,
                "message": "Token refreshed successfully.",
                "data": serializer.validated_data,
            },
            status=status.HTTP_200_OK,
        )

class CustomTokenVerifyView(TokenVerifyView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                "success": True,
                "message": "Token is valid.",
                "data": None,
            },
            status=status.HTTP_200_OK,
        )


