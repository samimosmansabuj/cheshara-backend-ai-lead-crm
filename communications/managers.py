from django.db import models

from .querysets import (
    ConversationQuerySet,
    MessageQuerySet,
    MessageStatusHistoryQuerySet,
    WebhookEventQuerySet,
    OutboundMessageQueueQuerySet,
    AIAnalysisQuerySet
)


class ConversationManager(models.Manager.from_queryset(ConversationQuerySet)):
    pass


class MessageManager(models.Manager.from_queryset(MessageQuerySet)):
    pass


class MessageStatusHistoryManager(
    models.Manager.from_queryset(MessageStatusHistoryQuerySet)
):
    pass

class AIAnalysisManager(models.Manager.from_queryset(AIAnalysisQuerySet)):
    pass

class WebhookEventManager(
    models.Manager.from_queryset(WebhookEventQuerySet)
):
    pass


class OutboundMessageQueueManager(
    models.Manager.from_queryset(OutboundMessageQueueQuerySet)
):
    pass

