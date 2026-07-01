from django.contrib import admin

from .models import (
    Organization,
    BusinessProfile,
    BusinessLink,
    BusinessAddress,
    BusinessSetting,
    ProviderAccount,
    PhoneNumber,
)


class BusinessLinkInline(admin.TabularInline):
    model = BusinessLink
    extra = 0


class BusinessAddressInline(admin.TabularInline):
    model = BusinessAddress
    extra = 0


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "country", "is_verified", "is_demo", "is_onboarding_completed", "status", "created_at")
    list_filter = ("country", "is_verified", "is_demo", "is_onboarding_completed", "status", "created_at")
    search_fields = ("name", "slug", "owner__phone_number", "owner__email")
    autocomplete_fields = ("owner",)
    list_select_related = ("owner",)
    readonly_fields = ("slug", "created_at", "updated_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 25


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ("organization", "business_type", "industry", "website", "created_at")
    list_filter = ("business_type", "industry")
    search_fields = ("organization__name", "email", "support_email")
    autocomplete_fields = ("organization",)
    list_select_related = ("organization",)
    inlines = (BusinessLinkInline, BusinessAddressInline)
    readonly_fields = ("created_at", "updated_at")


@admin.register(BusinessSetting)
class BusinessSettingAdmin(admin.ModelAdmin):
    list_display = ("organization", "language", "timezone", "currency", "reply_tone", "auto_reply_enabled")
    list_filter = ("language", "currency", "auto_reply_enabled")
    search_fields = ("organization__name",)
    autocomplete_fields = ("organization",)
    list_select_related = ("organization",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(ProviderAccount)
class ProviderAccountAdmin(admin.ModelAdmin):
    list_display = ("organization", "provider", "friendly_name", "status", "last_synced_at")
    list_filter = ("provider", "status")
    search_fields = ("friendly_name", "account_sid", "organization__name")
    autocomplete_fields = ("organization",)
    list_select_related = ("organization",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "organization", "provider", "country", "status", "is_primary", "last_synced_at")
    list_filter = ("status", "country", "is_primary")
    search_fields = ("phone_number", "provider_phone_sid", "organization__name")
    autocomplete_fields = ("organization", "provider")
    list_select_related = ("organization", "provider")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"


