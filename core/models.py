from django.db import models
from .choices import SettingValueType, NotificationType, NotificationPriority
from common.models import BaseModel

class Notification(BaseModel):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="notifications")
    organization = models.ForeignKey("business.Organization", on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    body = models.TextField()
    notification_type = models.CharField(max_length=30, choices=NotificationType.choices)
    priority = models.CharField(max_length=20, choices=NotificationPriority.choices, default=NotificationPriority.NORMAL)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    action_url = models.URLField(blank=True, default="")
    payload = models.JSONField(default=dict, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)

class AuditLog(BaseModel):
    organization = models.ForeignKey("business.Organization", on_delete=models.CASCADE, related_name="audit_logs")
    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs")
    action = models.CharField(max_length=100)
    module = models.CharField(max_length=100)
    object_type = models.CharField(max_length=100)
    object_id = models.UUIDField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    request_method = models.CharField(max_length=10)
    request_path = models.CharField(max_length=500)
    metadata = models.JSONField(default=dict, blank=True)

class SystemSetting(BaseModel):
    key = models.CharField(max_length=100, unique=True, db_index=True)
    value = models.JSONField(default=dict, blank=True)
    value_type = models.CharField(max_length=255, choices=SettingValueType.choices)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)

class APIKey(BaseModel):
    organization = models.ForeignKey("business.Organization", on_delete=models.CASCADE, related_name="api_keys")
    name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=128, unique=True, db_index=True)
    secret_key = models.CharField(max_length=255)
    permissions = models.JSONField(default=list, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


class BusinessType(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "Business Type"
        verbose_name_plural = "Business Types"

    def __str__(self):
        return self.name

class Industry(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=170, unique=True)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name




