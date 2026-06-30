from django.db import models
from .querysets import (
    OrganizationQuerySet, BusinessProfileQuerySet,
    PhoneNumberQuerySet, BusinessSettingQuerySet, ProviderAccountQuerySet
)


# ==========================================================
# Organization
class OrganizationManager(models.Manager.from_queryset(OrganizationQuerySet)):
    def get_queryset(self):
        return OrganizationQuerySet(
            self.model,
            using=self._db,
        )

    # -------------------------
    # QuerySet Proxy
    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        return self.get_queryset().inactive()

    def suspended(self):
        return self.get_queryset().suspended()

    def pending(self):
        return self.get_queryset().pending()

    def onboarded(self):
        return self.get_queryset().onboarded()

    def with_owner(self):
        return self.get_queryset().with_owner()

    def with_profile(self):
        return self.get_queryset().with_profile()

    def with_phone_numbers(self):
        return self.get_queryset().with_phone_numbers()

    def with_lead_count(self):
        return self.get_queryset().with_lead_count()

    def with_phone_count(self):
        return self.get_queryset().with_phone_count()
    
    # -------------------------

    # -------------------------
    # Factory
    def create_organization(self, **validated_data):
        return self.create(**validated_data)
    
     # -------------------------
# ==========================================================

# ==========================================================
# Business Profile
class BusinessProfileManager(models.Manager):
    def get_queryset(self):
        return BusinessProfileQuerySet(self.model, using=self._db,)

    def complete(self):
        return self.get_queryset().complete()

    def by_industry(self, industry):
        return self.get_queryset().by_industry(industry)

# ==========================================================

# ==========================================================
# Business Setting
class BusinessSettingManager(models.Manager):
    def get_queryset(self):
        return BusinessSettingQuerySet(self.model, using=self._db,)

    def auto_reply_enabled(self):
        return self.get_queryset().auto_reply_enabled()

    def push_notification_enabled(self):
        return self.get_queryset().push_notification_enabled()

# ==========================================================

# ==========================================================
# Business Setting
class ProviderAccountManager(models.Manager):
    def get_queryset(self):
        return ProviderAccountQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def suspended(self):
        return self.get_queryset().suspended()

    def disabled(self):
        return self.get_queryset().disabled()

    def pending(self):
        return self.get_queryset().pending()

    def failed(self):
        return self.get_queryset().failed()

    def by_provider(self, provider):
        return self.get_queryset().by_provider(provider)

# ==========================================================

# ==========================================================
# Phone Number
class PhoneNumberManager(models.Manager):
    def get_queryset(self):
        return PhoneNumberQuerySet(self.model, using=self._db,)

    def active(self):
        return self.get_queryset().active()

    def primary(self):
        return self.get_queryset().primary()

    def available(self):
        return self.get_queryset().available()

    def by_country(self, country):
        return self.get_queryset().by_country(country)

    def by_provider(self, provider):
        return self.get_queryset().by_provider(provider)

    # -------------------------
    # Factory
    # -------------------------
    def create_phone_number(self, **validated_data):
        return self.create(**validated_data)

# ==========================================================
