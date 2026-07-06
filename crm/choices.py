from django.db import models


class LeadStage(models.TextChoices):
    NEW = "new", "New"
    CONTACTED = "contacted", "Contacted"
    QUALIFIED = "qualified", "Qualified"
    HOT = "hot", "Hot"
    CONVERTED = "converted", "Converted"
    LOST = "lost", "Lost"


class LeadActivityType(models.TextChoices):
    CREATED = "created", "Created"
    MESSAGE_RECEIVED = "message_received", "Message Received"
    MESSAGE_SENT = "message_sent", "Message Sent"
    AI_REPLIED = "ai_replied", "AI Replied"
    STAGE_CHANGED = "stage_changed", "Stage Changed"
    TAG_ADDED = "tag_added", "Tag Added"
    TAG_REMOVED = "tag_removed", "Tag Removed"
    HANDOFF = "handoff", "Handoff"
    NOTE_ADDED = "note_added", "Note Added"

