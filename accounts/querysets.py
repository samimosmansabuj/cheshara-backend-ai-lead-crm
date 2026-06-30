from django.db import models
from django.utils import timezone
from datetime import timedelta


class UserQuerySet(models.QuerySet):

    def active(self):
        return self.filter(
            status="ACTIVE",
            is_deleted=False
        )

    def verified(self):
        return self.filter(
            is_phone_verified=True
        )

    def recently_active(self):
        return self.filter(
            last_activity_at__gte=timezone.now() - timedelta(days=7)
        )


