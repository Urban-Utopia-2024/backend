from celery import group, shared_task

from api.v1.utils import send_mail
from urban_utopia_2024.app_data import CHUNK_EMAIL
from user.models import User


@shared_task
def send_mass_mail(subject: str, message: str, user_emails: list[str]) -> None:
    """Отправляет письма указанным адресатам в user_emails."""
    for email in user_emails:
        send_mail(subject=subject, message=message, to=(email,))
    return


@shared_task
def send_mass_mail_async(subject: str, message: str) -> None:
    """Задача по рассылке писем пользователям."""
    user_emails: list[str] = User.objects.filter(
        is_staff=False,
        is_municipal=False,
    ).values_list(
        'email',
        flat=True,
    )
    user_groups: list[list[str]] = [
        user_emails[i:(i+CHUNK_EMAIL)] for
        i in range(0, len(user_emails), CHUNK_EMAIL)
    ]
    celery_group: group = group(
        send_mass_mail.s(
            subject=subject,
            message=message,
            user_emails=user_group
        ) for user_group in user_groups
    )
    celery_group.apply_async()
    return
