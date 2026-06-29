from django.db import models
from django.db.models import Count, Prefetch

from .choices import (
    OrganizationStatus,
    PhoneNumberStatus,
)


class OrganizationQuerySet(models.QuerySet):
    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    def active(self):
        return self.filter(status=OrganizationStatus.ACTIVE, is_deleted=False)

    def inactive(self):
        return self.filter(status=OrganizationStatus.INACTIVE, is_deleted=False)

    def suspended(self):
        return self.filter(status=OrganizationStatus.SUSPENDED, is_deleted=False)

    def pending(self):
        return self.filter(status=OrganizationStatus.PENDING, is_deleted=False)

    # --------------------------------------------------
    # Business
    # --------------------------------------------------

    def onboarded(self):
        return self.filter(is_onboarding_completed=True)

    def not_onboarded(self):
        return self.filter(is_onboarding_completed=False)

    # --------------------------------------------------
    # Relationships
    # --------------------------------------------------

    def with_owner(self):
        return self.select_related("owner")

    def with_profile(self):
        return self.select_related("business_profile")

    def with_phone_numbers(self):
        return self.prefetch_related("phone_numbers")

    # --------------------------------------------------
    # Dashboard Optimization
    # --------------------------------------------------

    def dashboard(self):
        return self.with_owner().with_profile().with_phone_numbers()

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    def with_lead_count(self):
        return self.annotate(lead_count=Count("leads", distinct=True))

    def with_phone_count(self):
        return self.annotate(phone_count=Count("phone_numbers", distinct=True))

class BusinessProfileQuerySet(models.QuerySet):
    def complete(self):
        return self.exclude(description="").exclude(website="")

    def by_industry(self, industry):
        return self.filter(industry=industry)

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

class BusinessSettingQuerySet(models.QuerySet):
    def auto_reply_enabled(self):
        return self.filter(auto_reply_enabled=True)

    def push_notification_enabled(self):
        return self.filter(push_notification=True)

