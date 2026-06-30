from django.db import models
from django.utils.text import slugify
from common.models import BaseModel
from accounts.models import User
from .choices import (
    OrganizationStatus, CountryCode, OnboardingStep, BusinessType, Industry, ProviderAccountStatus,
    Currency, DateFormat, Language, TimeFormat, AIReplyTone,PhoneProvider, PhoneNumberStatus
)
from .managers import OrganizationManager, ProviderAccountManager, BusinessProfileManager, BusinessSettingManager, PhoneNumberManager
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone



class Organization(BaseModel):
    owner = models.OneToOneField(User, on_delete=models.PROTECT, related_name="organization")
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    logo = models.ImageField(upload_to="organizations/logo/", blank=True, null=True)
    favicon = models.ImageField(upload_to="organizations/favicon/", blank=True, null=True)
    country = models.CharField(max_length=2, choices=CountryCode.choices, default=CountryCode.US, db_index=True)
    is_verified = models.BooleanField(default=False, help_text="Organization verification status.")
    is_demo = models.BooleanField(default=False, help_text="Used for demo/testing organizations.")
    is_onboarding_completed = models.BooleanField(default=False)
    onboarding_step = models.CharField(max_length=50, choices=OnboardingStep.choices, default=OnboardingStep.ACCOUNT_CREATED)

    objects = OrganizationManager()
    
    class Meta:
        db_table = "organizations"
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
        ordering = ["-created_at",]

        indexes = [
            models.Index(fields=["slug"], name="org_slug_idx"),
            models.Index(fields=["owner"], name="org_owner_idx"),
            models.Index(fields=["status"], name="org_status_idx"),
            models.Index(fields=["created_at"], name="org_created_idx"),
            models.Index(fields=["is_verified"], name="org_verified_idx"),
            models.Index(fields=["is_onboarding_completed"], name="org_onboarding_idx"),
        ]

        constraints = [
            models.UniqueConstraint(fields=["slug"], name="unique_organization_slug"),
            models.UniqueConstraint(fields=["owner"], name="unique_organization_owner"),
        ]

    def __str__(self):
        return self.name

    @property
    def logo_url(self):
        if self.logo:
            return self.logo.url
        return None
    
    @property
    def is_active(self):
        return (
            self.status == OrganizationStatus.ACTIVE
            and not self.is_deleted
        )
    
    @property
    def has_phone_number(self):
        return self.phone_numbers.filter(is_deleted=False).exists()
    
    @property
    def primary_phone(self):
        return self.phone_numbers.filter(is_primary=True, is_deleted=False).first()

    @property
    def lead_count(self):
        return self.leads.count()
    
    def clean(self):
        self.name = self.name.strip()
        if not self.name:
            raise ValidationError(
                {
                    "name": "Organization name cannot be empty."
                }
            )

        if len(self.name) < 3:
            raise ValidationError(
                {
                    "name": "Organization name must contain at least 3 characters."
                }
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Organization.objects.with_deleted().filter(
                slug=slug
            ).exclude(
                pk=self.pk
            ).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def complete_onboarding(self):
        self.is_onboarding_completed = True
        self.onboarding_step = OnboardingStep.COMPLETED
        self.save(update_fields=["is_onboarding_completed", "onboarding_step"])
        
    def activate(self):
        self.status = OrganizationStatus.ACTIVE
        self.save(update_fields=["status"])

    def suspend(self):
        self.status = OrganizationStatus.SUSPENDED
        self.save(update_fields=["status"])
    
    def deactivate(self):
        self.status = OrganizationStatus.INACTIVE
        self.save(update_fields=["status"])
    
    def update_logo(self, logo):
        self.logo = logo
        self.save(update_fields=["logo"])

    def update_favicon(self, favicon):
        self.favicon = favicon
        self.save(update_fields=["favicon"])
    
    def __repr__(self):
        return (
            f"<Organization("
            f"id={self.pk}, "
            f"name='{self.name}'"
            f")>"
        )

class BusinessProfile(BaseModel):
    organization = models.OneToOneField("business.Organization", on_delete=models.CASCADE, related_name="business_profile")
    business_type = models.CharField(max_length=30, choices=BusinessType.choices, default=BusinessType.COMPANY, db_index=True)
    industry = models.CharField(max_length=50, choices=Industry.choices, db_index=True)
    description = models.TextField(blank=True, default="")
    website = models.URLField(blank=True, default="")
    email = models.EmailField(blank=True, default="")
    support_email = models.EmailField(blank=True, default="")
    business_hours = models.JSONField(default=dict, blank=True, help_text="Weekly business working hours.")

    objects = BusinessProfileManager()

    class Meta:
        db_table = "business_profiles"
        verbose_name = "Business Profile"
        verbose_name_plural = "Business Profiles"
        ordering = ["organization__name"]
        indexes = [
            models.Index(fields=["industry"], name="bp_industry_idx"),
            models.Index(fields=["business_type"], name="bp_business_type_idx"),
        ]

    def __str__(self):
        return self.organization.name

    def clean(self):
        super().clean()
        if self.website:
            self.website = self.website.strip()
        if self.email:
            self.email = self.email.lower().strip()
        if self.support_email:
            self.support_email = self.support_email.lower().strip()

    @property
    def has_business_hours(self):
        return bool(self.business_hours)

class BusinessLink(BaseModel):
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name="links")
    title = models.CharField(max_length=50)
    url = models.URLField(max_length=255)

class BusinessAddress(BaseModel):
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name="addresss")
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True, default="")
    postal_code = models.CharField(max_length=30, blank=True, default="")
    country = models.CharField(max_length=2, db_index=True)
    
    @property
    def full_address(self):
        parts = [self.address_line_1, self.address_line_2, self.city, self.state, self.postal_code, self.country]
        return ", ".join(part for part in parts if part)

class BusinessSetting(BaseModel):
    organization = models.OneToOneField("business.Organization", on_delete=models.CASCADE, related_name="settings")
    language = models.CharField(max_length=10, choices=Language.choices, default=Language.ENGLISH)
    timezone = models.CharField(max_length=100, default="America/New_York")
    currency = models.CharField(max_length=10, choices=Currency.choices, default=Currency.USD)
    date_format = models.CharField(max_length=20, choices=DateFormat.choices, default=DateFormat.MM_DD_YYYY)
    time_format = models.CharField(max_length=10, choices=TimeFormat.choices, default=TimeFormat.HOUR_12)
    lead_hot_score = models.PositiveSmallIntegerField(default=80, validators=[MinValueValidator(1), MaxValueValidator(100)], help_text="Minimum AI score to consider a lead as HOT.")
    
    reply_tone = models.CharField(max_length=50, choices=AIReplyTone.choices, default=AIReplyTone.FRIENDLY)
    auto_reply_enabled = models.BooleanField(default=True)
    reply_speed = models.PositiveBigIntegerField(default=0)
    auto_follow_up = models.BooleanField(default=True)
    
    push_notification_enabled = models.BooleanField(default=True)
    email_notification_enabled = models.BooleanField(default=True)
    notification_sound = models.BooleanField(default=True)

    objects = BusinessSettingManager()

    class Meta:
        db_table = "business_settings"
        verbose_name = "Business Setting"
        verbose_name_plural = "Business Settings"
        ordering = ["organization__name"]
        indexes = [
            models.Index(fields=["language"], name="bs_language_idx"),
            models.Index(fields=["currency"], name="bs_currency_idx"),
            models.Index(fields=["auto_reply_enabled"], name="bs_auto_reply_idx"),
        ]

    def __str__(self):
        return f"{self.organization.name} Settings"

    def clean(self):
        super().clean()
        self.timezone = self.timezone.strip()

    @property
    def notifications_enabled(self):
        return self.push_notification_enabled or self.email_notification_enabled

class ProviderAccount(BaseModel):
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, related_name="provider_account")
    provider = models.CharField(max_length=20, choices=PhoneProvider.choices, default=PhoneProvider.TWILIO, db_index=True)
    account_sid = models.CharField(max_length=64, unique=True, db_index=True)
    friendly_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=ProviderAccountStatus.choices, default=ProviderAccountStatus.ACTIVE)
    webhook_url = models.URLField(blank=True, default="")
    webhook_secret = models.CharField(max_length=255, blank=True, default="")
    last_synced_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    objects = ProviderAccountManager()

    class Meta:
        db_table = "provider_accounts"

        indexes = [
            models.Index(fields=["provider", "status"], name="provider_status_idx"),
        ]

    def __str__(self):
        return f"{self.organization.name} ({self.provider})"

class PhoneNumber(BaseModel):
    organization = models.ForeignKey("business.Organization", on_delete=models.CASCADE, related_name="phone_numbers")
    provider = models.ForeignKey(ProviderAccount, on_delete=models.SET_NULL, blank=True, null=True)
    phone_number = models.CharField(max_length=30, unique=True, db_index=True)
    provider_phone_sid = models.CharField(max_length=100, unique=True, db_index=True)
    messaging_service_sid = models.CharField(max_length=100, blank=True, default="")
    country = models.CharField(max_length=2, db_index=True)
    region = models.CharField(max_length=100, blank=True, default="")
    capabilities = models.JSONField(default=dict, blank=True)
    configuration = models.JSONField(default=dict, blank=True)
    is_primary = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=PhoneNumberStatus.choices, default=PhoneNumberStatus.PENDING, db_index=True)
    purchased_at = models.DateTimeField(null=True, blank=True)
    released_at = models.DateTimeField(null=True, blank=True)
    last_synced_at = models.DateTimeField(default=timezone.now)
    objects = PhoneNumberManager()

    class Meta:
        db_table = "business_phone_numbers"
        verbose_name = "Phone Number"
        verbose_name_plural = "Phone Numbers"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["organization", "status"], name="phone_org_status_idx"),
            models.Index(fields=["provider", "provider_phone_sid"], name="phone_provider_idx"),
            models.Index(fields=["country"], name="phone_country_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "is_primary"], condition=models.Q(is_primary=True, is_deleted=False), name="unique_primary_phone_per_org"
            ),
        ]

    def __str__(self):
        return self.phone_number

    @property
    def is_active(self):
        return self.status == PhoneNumberStatus.ACTIVE and not self.is_deleted

    @property
    def sms_enabled(self):
        return self.capabilities.get("sms", False)

    @property
    def mms_enabled(self):
        return self.capabilities.get("mms", False)

    @property
    def voice_enabled(self):
        return self.capabilities.get("voice", False)

