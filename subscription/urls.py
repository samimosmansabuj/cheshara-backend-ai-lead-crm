from django.urls import path, include
from .views import SubscriptionPlanViewSet, UserSubscriptionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("subscription-plans", SubscriptionPlanViewSet, basename="subscription-plan")
router.register("user-subscription", UserSubscriptionViewSet, basename="user-subscription")

urlpatterns = [
    path("", include(router.urls)),
]
