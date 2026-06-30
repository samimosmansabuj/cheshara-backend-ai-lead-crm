from django.db import models


class ConversationStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    CLOSED = "closed", "Closed"
    ARCHIVED = "archived", "Archived"


class MessageDirection(models.TextChoices):
    INBOUND = "inbound", "Inbound"
    OUTBOUND = "outbound", "Outbound"


class MessageType(models.TextChoices):
    TEXT = "text", "Text"
    SYSTEM = "system", "System"
    TEMPLATE = "template", "Template"


class MessageStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    QUEUED = "queued", "Queued"
    SENT = "sent", "Sent"
    DELIVERED = "delivered", "Delivered"
    FAILED = "failed", "Failed"
    UNDELIVERED = "undelivered", "Undelivered"


class ProviderStatus(models.TextChoices):
    ACCEPTED = "accepted", "Accepted"
    QUEUED = "queued", "Queued"
    SENDING = "sending", "Sending"
    SENT = "sent", "Sent"
    DELIVERED = "delivered", "Delivered"
    FAILED = "failed", "Failed"
    UNDELIVERED = "undelivered", "Undelivered"
    READ = "read", "Read"


class SentimentType(models.TextChoices):
    VERY_POSITIVE = "very_positive", "Very Positive"
    POSITIVE = "positive", "Positive"
    NEUTRAL = "neutral", "Neutral"
    NEGATIVE = "negative", "Negative"
    VERY_NEGATIVE = "very_negative", "Very Negative"


class IntentType(models.TextChoices):
    GENERAL_INQUIRY = "general_inquiry", "General Inquiry"
    SERVICE_INQUIRY = "service_inquiry", "Service Inquiry"
    PRICE_INQUIRY = "price_inquiry", "Price Inquiry"
    BOOK_APPOINTMENT = "book_appointment", "Book Appointment"
    FOLLOW_UP = "follow_up", "Follow Up"
    COMPLAINT = "complaint", "Complaint"
    SUPPORT = "support", "Support"
    PURCHASE = "purchase", "Purchase"
    SPAM = "spam", "Spam"
    UNKNOWN = "unknown", "Unknown"


class ProviderType(models.TextChoices):
    TWILIO = "twilio", "Twilio"


class QueueStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    CANCELLED = "cancelled", "Cancelled"


class HandoffReason(models.TextChoices):
    HOT_LEAD = "hot_lead", "Hot Lead"
    CUSTOMER_REQUEST = "customer_request", "Customer Request"
    LOW_CONFIDENCE = "low_confidence", "Low Confidence"
    AI_FAILED = "ai_failed", "AI Failed"
    MANUAL = "manual", "Manual"

