from django.db import models
from django.utils.text import slugify
from common.models import BaseModel
from accounts.models import User
from .choices import (
    OrganizationStatus,
    CountryCode,
    OnboardingStep
)
from .managers import (
    OrganizationManager,
)
from django.core.exceptions import ValidationError


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
    onboarding_step = models.PositiveSmallIntegerField(default=1, help_text="Current onboarding step.")
    onboarding_step = models.CharField( max_length=50, choices=OnboardingStep.choices, default=OnboardingStep.ACCOUNT_CREATED)

    objects = OrganizationManager()
    
    class Meta:
        db_table = "organizations"

        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

        ordering = [
            "-created_at",
        ]

        indexes = [
            models.Index(
                fields=["slug"],
                name="org_slug_idx",
            ),
            models.Index(
                fields=["owner"],
                name="org_owner_idx",
            ),
            models.Index(
                fields=["status"],
                name="org_status_idx",
            ),
            models.Index(
                fields=["created_at"],
                name="org_created_idx",
            ),
            models.Index(
                fields=["is_verified"],
                name="org_verified_idx",
            ),
            models.Index(
                fields=["is_onboarding_completed"],
                name="org_onboarding_idx",
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["slug"],
                name="unique_organization_slug",
            ),
            models.UniqueConstraint(
                fields=["owner"],
                name="unique_organization_owner",
            ),
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
        return self.phone_numbers.filter(
            is_deleted=False
        ).exists()
    
    @property
    def primary_phone(self):
        return (
            self.phone_numbers
            .filter(
                is_primary=True,
                is_deleted=False,
            )
            .first()
        )
    
    @property
    def display_logo(self):
        if self.logo:
            return self.logo.url

        return None

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

        self.onboarding_step = (
            OnboardingStep.COMPLETED
        )

        self.save(
            update_fields=[
                "is_onboarding_completed",
                "onboarding_step",
            ]
        )
        
    def activate(self):

        self.status = OrganizationStatus.ACTIVE

        self.save(
            update_fields=[
                "status",
            ]
        )

    def suspend(self):

        self.status = OrganizationStatus.SUSPENDED

        self.save(
            update_fields=[
                "status",
            ]
        )
    
    def deactivate(self):

        self.status = OrganizationStatus.INACTIVE

        self.save(
            update_fields=[
                "status",
            ]
        )
    
    def update_logo(self, logo):

        self.logo = logo

        self.save(
            update_fields=[
                "logo",
            ]
        )

    def update_favicon(self, favicon):

        self.favicon = favicon

        self.save(
            update_fields=[
                "favicon",
            ]
        )
    
    def __repr__(self):

        return (
            f"<Organization("
            f"id={self.pk}, "
            f"name='{self.name}'"
            f")>"
        )


from django.core.validators import RegexValidator
from django.db import models

from common.models import BaseModel

from .choices import (
    BusinessType,
    Industry,
)
from .managers import BusinessProfileManager


class BusinessProfile(BaseModel):
    organization = models.OneToOneField("business.Organization", on_delete=models.CASCADE, related_name="business_profile")
    business_type = models.CharField(max_length=30, choices=BusinessType.choices, default=BusinessType.COMPANY, db_index=True)
    industry = models.CharField(max_length=50, choices=Industry.choices, db_index=True)
    description = models.TextField(blank=True, default="")
    website = models.URLField(blank=True, default="")
    email = models.EmailField(blank=True, default="")
    support_email = models.EmailField(blank=True, default="")
    country = models.CharField(max_length=2, db_index=True)
    business_hours = models.JSONField(default=dict, blank=True, help_text="Weekly business working hours.")
    holiday_schedule = models.JSONField(default=list, blank=True, help_text="Holiday list.")

    objects = BusinessProfileManager()

    class Meta:
        db_table = "business_profiles"
        verbose_name = "Business Profile"
        verbose_name_plural = "Business Profiles"

        ordering = ["organization__name"]

        indexes = [
            models.Index(
                fields=["industry"],
                name="bp_industry_idx",
            ),
            models.Index(
                fields=["business_type"],
                name="bp_business_type_idx",
            ),
            models.Index(
                fields=["country"],
                name="bp_country_idx",
            ),
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

    @property
    def has_google_business(self):
        return bool(self.google_business_url)

    @property
    def full_address(self):
        parts = [
            self.address_line_1,
            self.address_line_2,
            self.city,
            self.state,
            self.postal_code,
            self.country,
        ]

        return ", ".join(
            part for part in parts if part
        )

class BusinessLink(BaseModel):
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name="links")
    title = models.CharField(max_length=50)
    url = models.URLField(max_length=255)

class BusinessAddress(BaseModel):
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name="addresss")
    address_line_1 = models.CharField(max_length=255, blank=True, default="")
    address_line_2 = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="")
    state = models.CharField(max_length=100, blank=True, default="")
    postal_code = models.CharField(max_length=30, blank=True, default="")
