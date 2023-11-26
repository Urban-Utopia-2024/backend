import hashlib
import random
import string

from django.core import mail

from urban_utopia_2024.app_data import (
    DEFAULT_FROM_EMAIL, PASS_ITERATIONS, SECRET_SALT, USER_PASS_RAND_CYCLES,
)


def create_secret_code(email: str) -> str:
    """Создает случайный код на базе зерна хэш-значения email."""
    email_secret: str = f'{email}{SECRET_SALT}'
    for _ in range(PASS_ITERATIONS):
        email_secret: str = hashlib.sha256(email_secret.encode()).hexdigest()
    random.seed(email_secret)
    pass_chars: list[str] = []
    for _ in range(USER_PASS_RAND_CYCLES):
        lowercase: str = random.choice(string.ascii_lowercase)
        uppercase: str = random.choice(string.ascii_uppercase)
        digit: str = random.choice(string.digits)
        special: str = random.choice('!_@#$%^&+=')
        pass_chars.extend([lowercase, uppercase, digit, special])
    return ''.join(pass_chars)


def send_mail(subject: str, message: str, to: tuple[str]) -> None:
    """
    Отправляет электронное сообщение списку пользователей в to.
    Назначает subject темой письма и message текстом.

    "backend=None" означает, что бекенд будет выбран согласно указанному
    значению в settings.EMAIL_BACKEND.
    """
    with mail.get_connection(backend=None, fail_silently=False) as conn:
        mail.EmailMessage(
            subject=subject,
            body=message,
            from_email=DEFAULT_FROM_EMAIL,
            to=to,
            connection=conn
        ).send(fail_silently=False)
    return
