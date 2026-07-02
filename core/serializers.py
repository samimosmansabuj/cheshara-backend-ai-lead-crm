from rest_framework import serializers
from .models import BusinessType, Industry


class BusinessTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessType
        fields = ("id", "name", "slug", "description", "is_active", "sort_order")
        read_only_fields = ("id",)


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ("id", "name", "slug", "description", "is_active", "sort_order")
        read_only_fields = ("id",)


