from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    BusinessTypeViewSet,
    IndustryViewSet,
)

router = DefaultRouter()
router.register("business-types", BusinessTypeViewSet, basename="business-type")
router.register("industries", IndustryViewSet, basename="industry")

urlpatterns = [
    path("", include(router.urls)),
]

