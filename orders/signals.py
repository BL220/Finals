import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Order

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, created, **kwargs):
    if created:
        logger.info('New order #%s created by user "%s".', instance.pk, instance.user.username)
    else:
        logger.info('Order #%s status updated to "%s".', instance.pk, instance.status)


@receiver(post_save, sender=User)
def new_user_registered(sender, instance, created, **kwargs):
    if created:
        logger.info('New user registered: "%s".', instance.username)
