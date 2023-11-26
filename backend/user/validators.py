import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext

BUILDING_PATTERN: str = r'^\d{1,4}[А-Я]{0,1}$'
BUILDING_ERROR: str = gettext(
    'Введите корректный номер корпуса вида 123 или 123А.'
)
EMAIL_PATTERN: str = r'^(?!\.)[0-9A-Za-z\.]{1,50}@[a-zA-z]+\.[a-zA-z]+$'
EMAIL_ERROR: str = gettext(
    'Введите корректный email (например: example@example.ru)'
)
LAT_LON_PATTERN: str = r'^\d{2}.\d{0,6}'
LAT_ERR: str = gettext(
    'Укажите корректные координаты широты вида XX.XXXXXX.'
)
LON_ERR: str = gettext(
    'Укажите корректные координаты долготы вида XX.XXXXXX.'
)
PASS_PATTERN: str = (
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!_@#$%^&+=]).{5,512}$'
)
PASS_ERROR: str = gettext(
    'Введите пароль, который удовлетворяет критериям: '
    '- длина от 5 до 50 символов; '
    '- включает хотя бы одну цифру (0-9); '
    '- включает хотя бы одну прописную букву (a-z); '
    '- включает хотя бы одну заглавную букву (A-Z); '
    '- включает хотя бы один специальный символ (!_@#$%^&+=).'
)
USER_FIRST_NAME_PATTERN: str = r'^[А-ЯЁа-яё]{1,28}$'
USER_LAST_NAME_PATTERN: str = r'^[А-ЯЁа-яё][А-ЯЁа-яё\s\-]{1,28}[А-ЯЁа-яё]$'
USER_FIRST_NAME_ERROR: str = gettext(
    'Укажите корректное имя (например: Иван)'
)
USER_MID_NAME_ERROR: str = gettext(
    'Укажите корректное отчество (например: Ивановна)'
)
USER_LAST_NAME_ERROR: str = gettext(
    'Укажите корректную фамилию (например: Иванов или Иванова-Петрова)'
)


def validate_building(value: str) -> str:
    """Производит валидацию номера корпуса строения."""
    if re.fullmatch(BUILDING_PATTERN, value):
        return value
    raise ValidationError(BUILDING_ERROR)


def validate_email(value: str) -> str:
    """Производит валидацию электронной почты."""
    if re.fullmatch(EMAIL_PATTERN, value):
        return value
    raise ValidationError(EMAIL_ERROR)


def validate_first_name(value: str) -> str:
    """Производит валидацию имени пользователя."""
    if re.fullmatch(USER_FIRST_NAME_PATTERN, value):
        return value
    raise ValidationError(USER_FIRST_NAME_ERROR)


def validate_mid_name(value: str) -> str:
    """Производит валидацию отчества пользователя."""
    if value is None or re.fullmatch(USER_FIRST_NAME_PATTERN, value):
        return value
    raise ValidationError(USER_MID_NAME_ERROR)


def validate_last_name(value: str) -> str:
    """Производит валидацию фамилии пользователя."""
    if re.fullmatch(USER_LAST_NAME_PATTERN, value):
        return value
    raise ValidationError(USER_LAST_NAME_ERROR)


def validate_lat(value: float) -> float:
    """Производит валидацию координаты широты в десятичном представлении."""
    if re.fullmatch(LAT_LON_PATTERN, str(value)):
        return value
    raise ValidationError(LAT_ERR)


def validate_lon(value: float) -> float:
    """Производит валидацию координаты долготы в десятичном представлении."""
    if re.fullmatch(LAT_LON_PATTERN, str(value)):
        return value
    raise ValidationError(LON_ERR)


def validate_password(value: str) -> str:
    """Производит валидацию пароля пользователя."""
    if re.fullmatch(PASS_PATTERN, value):
        return value
    raise ValidationError(PASS_ERROR)
