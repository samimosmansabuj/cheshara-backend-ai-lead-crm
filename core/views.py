from rest_framework.viewsets import ModelViewSet
from core.utils.viewsets import OwnModelViewSet
from .models import BusinessType, Industry
from .permissions import AdminWritePermission
from .serializers import (
    BusinessTypeSerializer,
    IndustrySerializer,
)


class BusinessTypeViewSet(OwnModelViewSet):
    serializer_class = BusinessTypeSerializer
    permission_classes = [AdminWritePermission]
    queryset = BusinessType.objects.filter(is_active=True).order_by("sort_order", "name")


class IndustryViewSet(OwnModelViewSet):
    serializer_class = IndustrySerializer
    permission_classes = [AdminWritePermission]
    queryset = Industry.objects.filter(is_active=True).order_by("sort_order", "name")



# class SetUpNewPhoneNumber()


