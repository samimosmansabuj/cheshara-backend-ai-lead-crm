from django.db.models.signals import post_save
from django.dispatch import receiver

from business.models import Organization
from .models import UserNotificationSettings


@receiver(post_save, sender=Organization)
def create_user_notification_settings(sender, instance, created, **kwargs):
    if not created:
        return

    UserNotificationSettings.objects.get_or_create(
        organization=instance,
        defaults={
            "user": instance.owner,
        },
    )

