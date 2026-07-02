from django.urls import path
from business.views import BusinessProfileSetupAPIView, UserBusinessSettingAPIView, UserBusinessOnboardingAPIView, UserBusinessProfileAPIView

urlpatterns = [
    path("business/profile/setup/", BusinessProfileSetupAPIView.as_view(), name="business-profile-setup",),
    
    path("me/business-profile/", UserBusinessProfileAPIView.as_view(), name="user-business-profile"),
    path("me/business-settings/", UserBusinessSettingAPIView.as_view(), name="update-business-settings"),
    path("me/onboarding-status/", UserBusinessOnboardingAPIView.as_view(), name="onboarding-status"),
]
