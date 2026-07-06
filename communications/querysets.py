from django.db import models
from decimal import Decimal
from .choices import (
    ConversationStatus,
    MessageDirection,
    MessageStatus,
    QueueStatus,
    SentimentType, IntentType
)


class ConversationQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=ConversationStatus.ACTIVE)

    def closed(self):
        return self.filter(status=ConversationStatus.CLOSED)

    def archived(self):
        return self.filter(status=ConversationStatus.ARCHIVED)

class MessageQuerySet(models.QuerySet):
    def inbound(self):
        return self.filter(direction=MessageDirection.INBOUND)

    def outbound(self):
        return self.filter(direction=MessageDirection.OUTBOUND)

    def pending(self):
        return self.filter(status=MessageStatus.PENDING)

    def queued(self):
        return self.filter(status=MessageStatus.QUEUED)

    def delivered(self):
        return self.filter(status=MessageStatus.DELIVERED)

    def failed(self):
        return self.filter(status=MessageStatus.FAILED)

class MessageStatusHistoryQuerySet(models.QuerySet):
    def latest(self):
        return self.order_by("-occurred_at")

class WebhookEventQuerySet(models.QuerySet):
    def processed(self):
        return self.filter(processed=True)

    def pending(self):
        return self.filter(processed=False)

class OutboundMessageQueueQuerySet(models.QuerySet):
    def pending(self):
        return self.filter(status=QueueStatus.PENDING)

    def processing(self):
        return self.filter(status=QueueStatus.PROCESSING)

    def completed(self):
        return self.filter(status=QueueStatus.COMPLETED)

    def failed(self):
        return self.filter(status=QueueStatus.FAILED)

class AIAnalysisQuerySet(models.QuerySet):
    def positive(self):
        return self.filter(
            sentiment__in=[
                SentimentType.POSITIVE,
                SentimentType.VERY_POSITIVE,
            ]
        )

    def negative(self):
        return self.filter(
            sentiment__in=[
                SentimentType.NEGATIVE,
                SentimentType.VERY_NEGATIVE,
            ]
        )

    def neutral(self):
        return self.filter(
            sentiment=SentimentType.NEUTRAL,
        )

    def by_intent(self, intent: str):
        return self.filter(intent=intent)

    def purchase_intent(self):
        return self.filter(intent=IntentType.PURCHASE)

    def appointment_intent(self):
        return self.filter(intent=IntentType.BOOK_APPOINTMENT)

    def support_intent(self):
        return self.filter(intent=IntentType.SUPPORT)

    def high_confidence(self, score: float = 80):
        return self.filter(confidence_score__gte=Decimal(str(score)))

    def low_confidence(self, score: float = 50):
        return self.filter(confidence_score__lt=Decimal(str(score)))

    def high_score(self, score: int = 80):
        return self.filter(lead_score__gte=score)

    def low_score(self, score: int = 30):
        return self.filter(lead_score__lt=score)

    def slow_processing(self, milliseconds: int = 3000):
        return self.filter(processing_time_ms__gte=milliseconds)

    def latest(self):
        return self.order_by("-analyzed_at")

