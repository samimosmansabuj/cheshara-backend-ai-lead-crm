from django.db import models

from .choices import AIRequestStatus


class AIConfigurationQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class PromptTemplateQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def default(self):
        return self.filter(is_default=True)


class AIAnalysisQuerySet(models.QuerySet):
    def hot_leads(self):
        return self.filter(lead_stage="hot")


class AIUsageLogQuerySet(models.QuerySet):
    def completed(self):
        return self.filter(status=AIRequestStatus.COMPLETED)

    def failed(self):
        return self.filter(status=AIRequestStatus.FAILED)


class AIModelLogQuerySet(models.QuerySet):
    def completed(self):
        return self.filter(status=AIRequestStatus.COMPLETED)

    def failed(self):
        return self.filter(status=AIRequestStatus.FAILED)


