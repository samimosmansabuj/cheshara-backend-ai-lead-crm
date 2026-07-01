from django.contrib import admin

from .models import (
    Conversation, Message, MessageAttachment,
    AIAnalysis, HandoffEvent, WebhookEvent, OutboundMessageQueue, MessageTemplate,
)


class MessageAttachmentInline(admin.TabularInline):
    model = MessageAttachment
    extra = 0
    fields = ("file", "file_name", "file_type", "file_size", "provider_media_sid")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "lead", "organization", "status", "total_messages", "unread_messages", "ai_enabled", "last_message_at", "created_at")
    list_filter = ("status", "ai_enabled", "created_at")
    search_fields = ("lead__contact_number", "organization__name")
    autocomplete_fields = ("organization", "lead")
    list_select_related = ("organization", "lead")
    readonly_fields = ("started_at", "last_message_at", "created_at", "updated_at")
    ordering = ("-last_message_at",)
    date_hierarchy = "started_at"
    list_per_page = 25


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "provider_message_sid", "conversation", "lead", "direction", "message_type", "status", "is_ai_generated", "created_at")
    list_filter = ("direction", "message_type", "status", "is_ai_generated", "created_at")
    search_fields = ("provider_message_sid", "content", "sender", "recipient", "lead__contact_number")
    autocomplete_fields = ("conversation", "lead")
    list_select_related = ("conversation", "lead")
    readonly_fields = ("provider_message_sid", "sent_at", "delivered_at", "read_at", "created_at", "updated_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 25
    inlines = (MessageAttachmentInline,)


@admin.register(MessageAttachment)
class MessageAttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "file_name", "file_type", "file_size", "provider_media_sid", "created_at")
    search_fields = ("file_name", "provider_media_sid", "message__provider_message_sid")
    autocomplete_fields = ("message",)
    list_select_related = ("message",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 25


@admin.register(AIAnalysis)
class AIAnalysisAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "sentiment", "intent", "lead_score", "confidence_score", "ai_model", "processing_time_ms", "analyzed_at")
    list_filter = ("sentiment", "intent", "ai_model", "analyzed_at")
    search_fields = ("message__provider_message_sid", "summary", "suggested_reply")
    autocomplete_fields = ("message",)
    list_select_related = ("message",)
    readonly_fields = [field.name for field in AIAnalysis._meta.fields]
    ordering = ("-analyzed_at",)
    date_hierarchy = "analyzed_at"
    list_per_page = 25

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HandoffEvent)
class HandoffEventAdmin(admin.ModelAdmin):
    list_display = ("id", "lead", "conversation", "reason", "ai_score", "handed_off_at")
    list_filter = ("reason", "handed_off_at")
    search_fields = ("lead__contact_number", "conversation__id")
    autocomplete_fields = ("lead", "conversation")
    list_select_related = ("lead", "conversation")
    readonly_fields = [field.name for field in HandoffEvent._meta.fields]
    ordering = ("-handed_off_at",)
    date_hierarchy = "handed_off_at"
    list_per_page = 25

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    list_display = ("id", "organization", "provider", "event_type", "processed", "processed_at", "created_at")
    list_filter = ("provider", "processed", "created_at")
    search_fields = ("organization__name", "event_type", "error_message")
    autocomplete_fields = ("organization",)
    list_select_related = ("organization",)
    readonly_fields = [field.name for field in WebhookEvent._meta.fields]
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 25

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(OutboundMessageQueue)
class OutboundMessageQueueAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "priority", "retry_count", "max_retry", "status", "scheduled_at", "processed_at", "created_at")
    list_filter = ("status", "priority", "created_at")
    search_fields = ("message__provider_message_sid", "message__lead__contact_number", "last_error")
    autocomplete_fields = ("message",)
    list_select_related = ("message",)
    readonly_fields = [field.name for field in OutboundMessageQueue._meta.fields]
    ordering = ("-scheduled_at",)
    date_hierarchy = "scheduled_at"
    list_per_page = 25

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "organization", "category", "is_active", "created_at")
    list_filter = ("category", "is_active", "created_at")
    search_fields = ("name", "content", "organization__name")
    autocomplete_fields = ("organization",)
    list_select_related = ("organization",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)
    date_hierarchy = "created_at"
    list_per_page = 25




