from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out

from .models import LogRecord


@receiver(user_logged_in)
def user_logged_in(sender, request, user, **kwargs):
    LogRecord.objects.create(user=user.username)


@receiver(user_logged_out)
def user_logged_out(sender, request, user, **kwargs):
    set_last_activity(user.username)


def set_last_activity(username):
    lr = LogRecord.objects.filter(
        user=username).last()
    if lr:
        lr.check_out = timezone.now()
        lr.save()
