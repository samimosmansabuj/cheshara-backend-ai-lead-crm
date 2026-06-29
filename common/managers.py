from django.db import models
from .querysets import BaseQuerySet

class BaseManager(models.Manager):
    def get_queryset(self):
        return (BaseQuerySet(self.model, using=self._db,).alive())

    def with_deleted(self):
        return BaseQuerySet(self.model, using=self._db,)

    def deleted(self):
        return self.with_deleted().deleted()

    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        return self.get_queryset().inactive()

    def suspended(self):
        return self.get_queryset().suspended()

