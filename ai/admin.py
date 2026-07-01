from django.contrib import admin

from .models import (
    AIConfiguration,
    PromptTemplate,
    AIUsageLog,
    AIModelLog,
)


@admin.register(AIConfiguration)
class AIConfigurationAdmin(admin.ModelAdmin):
    list_display = ("id", "organization", "provider", "model_name", "temperature", "max_tokens", "auto_reply_enabled", "is_active", "created_at")
    list_filter = ("provider", "auto_reply_enabled", "is_active", "created_at")
    search_fields = ("organization__name", "model_name")
    autocomplete_fields = ("organization",)
    list_select_related = ("organization",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("organization__name",)
    list_per_page = 25

@admin.register(PromptTemplate)
class PromptTemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "organization", "prompt_type", "is_default", "is_active", "created_at")
    list_filter = ("prompt_type", "is_default", "is_active", "created_at")
    search_fields = ("name", "content", "organization__name")
    autocomplete_fields = ("organization",)
    list_select_related = ("organization",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)
    list_per_page = 25

@admin.register(AIUsageLog)
class AIUsageLogAdmin(admin.ModelAdmin):
    list_display = ("id", "organization", "provider", "model_name", "prompt_tokens", "completion_tokens", "total_tokens", "estimated_cost", "processing_time", "status", "created_at")
    list_filter = ("provider", "status", "created_at")
    search_fields = ("organization__name", "model_name")
    autocomplete_fields = ("organization", "message")
    list_select_related = ("organization", "message")
    readonly_fields = [field.name for field in AIUsageLog._meta.fields]
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 25

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(AIModelLog)
class AIModelLogAdmin(admin.ModelAdmin):
    list_display = ("id", "organization", "provider", "model_name", "latency", "status", "created_at")
    list_filter = ("provider", "status", "created_at")
    search_fields = ("organization__name", "model_name", "response_text", "error_message")
    autocomplete_fields = ("organization", "message")
    list_select_related = ("organization", "message")
    readonly_fields = [field.name for field in AIModelLog._meta.fields]
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 25

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


