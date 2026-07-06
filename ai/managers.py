from django.db import models

from .querysets import (
    AIConfigurationQuerySet,
    PromptTemplateQuerySet,
    AIAnalysisQuerySet,
    AIUsageLogQuerySet,
    AIModelLogQuerySet,
)


class AIConfigurationManager(
    models.Manager.from_queryset(AIConfigurationQuerySet)
):
    pass


class PromptTemplateManager(
    models.Manager.from_queryset(PromptTemplateQuerySet)
):
    pass


class AIAnalysisManager(
    models.Manager.from_queryset(AIAnalysisQuerySet)
):
    pass


class AIUsageLogManager(
    models.Manager.from_queryset(AIUsageLogQuerySet)
):
    pass


class AIModelLogManager(
    models.Manager.from_queryset(AIModelLogQuerySet)
):
    pass


