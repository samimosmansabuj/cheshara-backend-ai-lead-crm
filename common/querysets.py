from django.db import models
from django.utils import timezone


from django.db import models
from django.utils import timezone


class BaseQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status="ACTIVE",is_deleted=False,)

    def inactive(self):
        return self.filter(status="INACTIVE",is_deleted=False,)

    def suspended(self):
        return self.filter(status="SUSPENDED",is_deleted=False,)

    def deleted(self):
        return self.filter(is_deleted=True,)

    def alive(self):
        return self.filter(is_deleted=False,)

    def soft_delete(self):
        return self.update(is_deleted=True,deleted_at=timezone.now(),)

    def restore(self):
        return self.update(is_deleted=False,deleted_at=None,)

