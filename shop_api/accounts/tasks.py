from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import ConfirmationCode


@shared_task
def clear_expired_confirmation_codes(hours: int = 24) -> str:
    """Удаляет коды подтверждения, которым больше заданного количества часов."""
    threshold = timezone.now() - timedelta(hours=hours)
    deleted_count, _ = ConfirmationCode.objects.filter(created_at__lt=threshold).delete()
    return f'Удалено просроченных кодов: {deleted_count}.'


@shared_task
def send_welcome_email(email: str, username: str) -> str:
    """Пример SMTP-задачи: отправка приветственного письма."""
    send_mail(
        subject='Добро пожаловать в Shop API',
        message=f'Привет, {username}! Спасибо за регистрацию в нашем магазине.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return f'Приветственное письмо отправлено на {email}.'