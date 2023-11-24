import os
from pathlib import Path

from dotenv import load_dotenv


"""App data."""


BASE_DIR: Path = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'), verbose=True)


"""Django data."""


DB_ENGINE: str = os.getenv('DB_ENGINE')
DB_USER: str = os.getenv('POSTGRES_USER')
DB_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
DB_HOST: str = os.getenv('DB_HOST')
DB_PORT: str = os.getenv('DB_PORT')
DB_NAME: str = os.getenv('POSTGRES_DB')

DATABASE_POSTGRESQL: dict[str, dict[str, str]] = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

DATABASE_SQLITE: dict[str, dict[str, str]] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


"""Models data."""


ADMIN_LIST_PER_PAGE: int = 15

ADDRESS_CITY_MAX_LEN: int = 50
ADDRESS_DISTRICT_MAX_LEN: int = 50
ADDRESS_STREET_MAX_LEN: int = 50
ADDRESS_HOUSE_MAX_VAL: int = 999
ADDRESS_BUILDING_MAX_LEN: int = 5
ADDRESS_ENTRANCE_MAX_VAL: int = 50
ADDRESS_FLOOR_MAX_VAL: int = 150
ADDRESS_APARTMENT_MAX_VAL: int = 9999
ADDRESS_INDEX_MAX_VAL: int = 999999

APPEAL_RATING_MAX_VAL: int = 10
APPEAL_RATING_MESSAGE: str = 'Оценка не может быть меньше 0 и больше 10.'
APPEAL_STAGE_INITIAL: str = 'initial'
APPEAL_STAGE_IN_PROGRESS: str = 'in_progress'
APPEAL_STAGE_COMPLETED: str = 'completed'
APPEAL_STAGE_REJECTED: str = 'rejected'
APPEAL_STATUS_CHOICES: list[tuple[str]] = [
    (APPEAL_STAGE_INITIAL, 'Подано'),
    (APPEAL_STAGE_IN_PROGRESS, 'На рассмотрения'),
    (APPEAL_STAGE_COMPLETED, 'Завершено'),
    (APPEAL_STAGE_REJECTED, 'Отклонено'),
]
APPEAL_STATUS_MAX_LEN: int = 20
APPEAL_TEXT_MAX_LEN: int = 2048
APPEAL_TOPIC_MAX_LEN: int = 50

NEWS_CATEGORY_MAX_LEN: int = 10
NEWS_CATEGORY_CHOICES: list[tuple[str]] = [
    ('Gas', 'Газ'),
    ('Heating', 'Отопление'),
    ('Light', 'Свет'),
    ('Other', 'Прочее'),
    ('Street', 'Улица'),
    ('Water', 'Вода'),
]

NEWS_COMMENT_MAX_LEN: int = 128
NEWS_COMMENT_SLICE: int = 15
NEWS_PICTURES_PATH: str = 'news/pictures/'
NEWS_TEXT_MAX_LEN: int = 2048

QUIZ_ANSWER_MAX_LEN: int = 100
QUIZ_ANSWER_SLICE: int = 10
QUIZ_TITLE_MAX_LEN: int = 50

TASK_TITLE_MAX_LEN: int = 50

USER_FULL_EMAIL_MAX_LEN: int = 150
USER_NAME_MAX_LEN: int = 30
# WARNING: Не изменять! Это максимальная длина хеша пароля Django.
USER_PASS_MAX_LEN: int = 512
USER_PHOTO_PATH: str = 'users/avatars/'
USER_RATING_MAX_VAL: float = 100.0


"""Security data."""

CITE_DOMAIN: str = os.getenv('CITE_DOMAIN')
CITE_IP: str = os.getenv('CITE_IP')

SECRET_KEY: str = os.getenv('SECRET_KEY')
