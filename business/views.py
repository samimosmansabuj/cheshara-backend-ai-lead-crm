from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from business.models import BusinessSetting
from core.utils.views import BaseCreateAPIView, BaseGetAPIView, BasePatchAPIView
from .serializers import OrganizationSetupSerializer, UpdateBusinessSettingSerializer, OrganizationSerializer
from .choices import OnboardingStep
from django.db import transaction
from rest_framework.exceptions import ValidationError, NotFound
from core.permissions import IsClientUser

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



