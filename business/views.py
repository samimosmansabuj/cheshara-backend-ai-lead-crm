from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from business.models import BusinessSetting
from core.utils.views import BaseCreateAPIView, BaseGetAPIView, BasePatchAPIView
from rest_framework.viewsets import GenericViewSet
from .serializers import (
    OrganizationSetupSerializer, UpdateBusinessSettingSerializer, OrganizationSerializer, UserNotificationSettingsSerializer,

    UserNotificationSettings, NotificationToggleSerializer
)
from .choices import OnboardingStep
from django.db import transaction
from rest_framework.exceptions import ValidationError, NotFound
from core.permissions import IsClientUser
from rest_framework.decorators import action


class BusinessProfileSetupAPIView(BaseCreateAPIView):
    serializer_class = OrganizationSetupSerializer
    permission_classes = [IsAuthenticated, IsClientUser]

    def create_perform(self, serializer):
        with transaction.atomic():
            organization = serializer.save()
            organization.onboarding_step = OnboardingStep.ACCOUNT_CREATED
            organization.save(update_fields=["onboarding_step"])
            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    "success": True,
                    "message": "Business profile created successfully.",
                    "data": OrganizationSetupSerializer(organization).data,
                }, status=status.HTTP_201_CREATED, headers=headers
            )

class UserBusinessOnboardingAPIView(APIView):
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            organization = user.organization
            return Response(
                {
                    "success": True,
                    "data": {
                        "onboarding_step": organization.onboarding_step,
                    }
                }, status=status.HTTP_200_OK
            )
        except AttributeError:
            raise NotFound("Business profile not found.", status.HTTP_404_NOT_FOUND)

class UserBusinessProfileAPIView(APIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated, IsClientUser]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            organization = user.organization
            serializer = self.serializer_class(organization, context={"request": request})
            return Response(
                {
                    "success": True,
                    "data": serializer.data
                }, status=status.HTTP_200_OK
            )
        except AttributeError:
            raise NotFound("Business profile not found.", status.HTTP_404_NOT_FOUND)

    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        user = request.user
        try:
            organization = user.organization
            serializer = self.serializer_class(organization, data=request.data, partial=True, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Business profile updated successfully.",
                    "data": serializer.data
                }, status=status.HTTP_200_OK
            )
        except AttributeError:
            raise NotFound("Business profile not found.", status.HTTP_404_NOT_FOUND)

class UserBusinessSettingAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            business_setting = BusinessSetting.objects.get(user=user)
            serializer = UpdateBusinessSettingSerializer(business_setting)
            return Response(
                {
                    "success": True,
                    "data": serializer.data
                }, status=status.HTTP_200_OK
            )
        except BusinessSetting.DoesNotExist:
            raise NotFound("Business setting not found.", status.HTTP_404_NOT_FOUND)
    
    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        user = request.user
        try:
            business_setting = BusinessSetting.objects.get(user=user)
            serializer = UpdateBusinessSettingSerializer(business_setting, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Business settings updated successfully.",
                    "data": serializer.data
                }, status=status.HTTP_200_OK
            )
        except BusinessSetting.DoesNotExist:
            raise NotFound("Business setting not found.", status.HTTP_404_NOT_FOUND)

class UserNotificationSettingsViewSet(GenericViewSet):
    serializer_class = UserNotificationSettingsSerializer
    permission_classes = [IsAuthenticated, IsClientUser]

    def get_object(self):
        organization = self.request.user.organization
        if organization:
            user_notification, _ = UserNotificationSettings.objects.get_or_create(
                user=self.request.user, organization=organization
            )
        else:
            user_notification, _ = UserNotificationSettings.objects.get_or_create(
                user=self.request.user
            )
        return user_notification

    @action(detail=False, methods=["get"], url_path="current")
    def current(self, request):
        serializer = self.get_serializer(self.get_object())
        return Response(
            {
                "success": True,
                "data": serializer.data,
            }
        )

    @action(detail=False, methods=["patch"], url_path="all-notification")
    def update_all_notification(self, request):
        setting = self.get_object()
        serializer = self.get_serializer(setting, data=request.data)
        serializer.is_valid(raise_exception=True)
        all_notification = serializer.validated_data.get("all_notification")
        
        setting.all_notification = all_notification
        setting.push_notification_enabled = all_notification
        setting.email_alert_enabled = all_notification
        setting.sms_alert_enabled = all_notification
        setting.instant_lead_alert = all_notification
        setting.weekly_performance_report = all_notification
        setting.save()

        return Response(
            {
                "success": True,
                "message": "Notification settings updated.",
                "data": self.get_serializer(setting).data,
            }
        )

    @action(detail=False, methods=["patch"], url_path="toggle")
    def toggle(self, request):
        serializer = NotificationToggleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        field = serializer.validated_data["field"]
        value = serializer.validated_data["value"]

        setting = self.get_object()

        setattr(setting, field, value)

        setting.all_notification = all([
            setting.push_notification_enabled,
            setting.email_alert_enabled,
            setting.sms_alert_enabled,
            setting.instant_lead_alert,
            setting.weekly_performance_report,
        ])

        setting.save()

        return Response(
            {
                "success": True,
                "message": f"{field} updated successfully.",
                "data": self.get_serializer(setting).data,
            },
            status=status.HTTP_200_OK,
        )


