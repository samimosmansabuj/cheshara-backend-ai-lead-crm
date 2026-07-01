from django.db import models
from django.db.models import Count

from .choices import (
    OrganizationStatus,
    PhoneNumberStatus,
    ProviderAccountStatus
)

class OrganizationQuerySet(models.QuerySet):
    # Status ==============================================
    def active(self):
        return self.filter(
            status=OrganizationStatus.ACTIVE,
            is_deleted=False,
        )

    def inactive(self):
        return self.filter(
            status=OrganizationStatus.INACTIVE,
            is_deleted=False,
        )

    def suspended(self):
        return self.filter(
            status=OrganizationStatus.SUSPENDED,
            is_deleted=False,
        )

    def pending(self):
        return self.filter(
            status=OrganizationStatus.PENDING,
            is_deleted=False,
        )

    # Onboarding ==============================================
    def onboarded(self):
        return self.filter(
            is_onboarding_completed=True,
            is_deleted=False,
        )

    def not_onboarded(self):
        return self.filter(
            is_onboarding_completed=False,
            is_deleted=False,
        )

    # Business ==============================================
    def verified(self):
        return self.filter(
            is_verified=True,
            is_deleted=False,
        )

    def demo(self):
        return self.filter(
            is_demo=True,
            is_deleted=False,
        )

    def by_country(self, country):
        return self.filter(
            country=country,
            is_deleted=False,
        )

    def by_industry(self, industry):
        return self.filter(
            industry=industry,
            is_deleted=False,
        )

    def by_business_type(self, business_type):
        return self.filter(
            business_type=business_type,
            is_deleted=False,
        )

    # Relationships ==============================================
    def with_owner(self):
        return self.select_related("owner")

    def with_phone_numbers(self):
        return self.prefetch_related("phone_numbers")

    def with_leads(self):
        return self.prefetch_related("leads")

    # Dashboard ==============================================
    def dashboard(self):
        return (
            self.with_owner()
            .with_phone_numbers()
            .with_leads()
            .with_lead_count()
            .with_phone_count()
        )

    # Statistics ==============================================
    def with_lead_count(self):
        return self.annotate(
            lead_count=Count(
                "leads",
                distinct=True,
            )
        )

    def with_phone_count(self):
        return self.annotate(
            phone_count=Count(
                "phone_numbers",
                distinct=True,
            )
        )

class BusinessSettingQuerySet(models.QuerySet):
    def auto_reply_enabled(self):
        return self.filter(auto_reply_enabled=True)

    def push_notification_enabled(self):
        return self.filter(push_notification=True)

class ProviderAccountQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=ProviderAccountStatus.ACTIVE, is_deleted=False)

    def suspended(self):
        return self.filter(status=ProviderAccountStatus.SUSPENDED, is_deleted=False)

    def disabled(self):
        return self.filter(status=ProviderAccountStatus.DISABLED, is_deleted=False)

    def pending(self):
        return self.filter(status=ProviderAccountStatus.PENDING, is_deleted=False)

    def failed(self):
        return self.filter(status=ProviderAccountStatus.FAILED, is_deleted=False)

    def by_provider(self, provider):
        return self.filter(provider=provider)

class PhoneNumberQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=PhoneNumberStatus.ACTIVE, is_deleted=False)

    def primary(self):
        return self.filter(is_primary=True)

    def available(self):
        return self.filter(organization__isnull=True)

    def by_country(self, country):
        return self.filter(country=country)

    def by_provider(self, provider):
        return self.filter(provider=provider)


