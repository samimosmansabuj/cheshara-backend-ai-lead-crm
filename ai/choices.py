from django.db import models


class AIProvider(models.TextChoices):
    OPENAI = "openai", "OpenAI"
    GEMINI = "gemini", "Google Gemini"
    CLAUDE = "claude", "Anthropic Claude"


class PromptType(models.TextChoices):
    SYSTEM = "system", "System"
    GREETING = "greeting", "Greeting"
    QUALIFICATION = "qualification", "Qualification"
    FOLLOW_UP = "follow_up", "Follow Up"
    CLOSING = "closing", "Closing"
    FALLBACK = "fallback", "Fallback"
    CUSTOM = "custom", "Custom"


class AIRequestStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"


