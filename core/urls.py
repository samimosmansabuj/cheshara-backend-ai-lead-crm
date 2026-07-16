from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    BusinessTypeViewSet,
    IndustryViewSet,
    FreeTrailPhoneNumberViewSet,
    TwilioWebhookHandler
)

router = DefaultRouter()
router.register("business-types", BusinessTypeViewSet, basename="business-type")
router.register("industries", IndustryViewSet, basename="industry")
router.register("free-trail-number", FreeTrailPhoneNumberViewSet, basename="free-trail-number")

urlpatterns = [
    path("", include(router.urls)),
    
    path("twilio/webhook/", TwilioWebhookHandler.as_view(), name="twilio-webhook",),
]

