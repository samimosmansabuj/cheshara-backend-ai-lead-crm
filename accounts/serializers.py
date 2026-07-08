from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, OTPVerification
from .choices import UserType
from business.models import Organization


class ClientSendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=30)

    def validate_phone_number(self, value):
        return value.strip()

class ClientVerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=30)
    otp = serializers.CharField(max_length=10)

    def validate(self, attrs):
        phone = attrs["phone_number"]
        otp = attrs["otp"]
        otp_obj = (
            OTPVerification.objects
            .filter(phone_number=phone, is_used=False,)
            .order_by("-created_at")
            .first()
        )
        if not otp_obj:
            raise serializers.ValidationError("OTP not found.")
        success, message = otp_obj.verify(otp)
        if not success:
            raise serializers.ValidationError(message)
        attrs["otp_obj"] = otp_obj
        return attrs

    def create(self, validated_data):
        phone = validated_data["phone_number"]
        user, created = User.objects.get_or_create(
            phone_number=phone,
            defaults={
                "user_type": UserType.CLIENT,
                "is_phone_verified": True,
            },
        )
        
        if not created and not user.is_phone_verified:
            user.is_phone_verified = True
            user.save(update_fields=["is_phone_verified"])

        refresh = RefreshToken.for_user(user)
        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

class AdminLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs["phone_number"].strip()
        password = attrs["password"]
        user = authenticate(username=phone_number, password=password,)
        if user is None:
            raise serializers.ValidationError("Invalid credentials.")

        if not user.is_staff:
            raise serializers.ValidationError("Permission denied.")

        refresh = RefreshToken.for_user(user)
        attrs["user"] = user
        attrs["access"] = str(refresh.access_token)
        attrs["refresh"] = str(refresh)
        return attrs


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "phone_number", "email", "full_name", "country_code", "profile_picture", "user_type", "is_phone_verified", "last_activity_at")


