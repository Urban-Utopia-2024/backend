import os
from pathlib import Path

from dotenv import load_dotenv


"""App data."""


BASE_DIR: Path = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'), verbose=True)

DEBUG = os.getenv('DB_ENGINE')
if DEBUG == 'True':
    DEBUG: bool = True
else:
    DEBUG: bool = False


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


"""Email data."""


EMAIL_CODE_LENGTH: int = 8

DEFAULT_FROM_EMAIL: str = os.getenv('DEFAULT_FROM_EMAIL')

PASSWORD_RESET_LINK: str = None

EMAIL_CONFIRM_EMAIL_SUBJECT: str = 'Подтверждение почты | Информационный портал'  # noqa (E501)

EMAIL_CONFIRM_EMAIL_TEXT: str = (
    'Добро пожаловать на сайт информационного портала г. Екатеринбурга!'
    '\n\n'
    'Для подтверждения электронной почты пожалуйста введите '
    'в появившемся окне на сайте код, указанный ниже:'
    '\n\n'
    '{secret_code}'
    '\n\n'
    'С наилучшими пожеланиями,\n'
    'Команда администрации г. Екатеринбурга.'
)

EMAIL_REGISTER_SUBJECT: str = 'Добро пожаловать | Информационный портал'

EMAIL_REGISTER_TEXT: str = (
    'Уважаемый {first_name} {last_name},'
    '\n\n'
    'Добро пожаловать на наш информационный портал, посвященный '
    'административным новостям г. Екатеринбурга! Мы рады приветствовать '
    'вас в нашем сообществе, где вы сможете быть в курсе последних событий, '
    'связанных с жизнью города, а также воспользоваться удобными сервисами '
    'для подачи заявлений и получения актуальной информации.'
    '\n\n'
    'Что вас ждет на нашем портале:\n'
    '- актуальные новости: Будьте в курсе всех событий города, следите за '
    'обновлениями и изменениями в административной сфере.\n'
    '- подача заявлений: Воспользуйтесь удобным сервисом для подачи различных '
    'заявлений онлайн. Это быстро, удобно и без лишних хлопот.\n'
    '- информационные ресурсы: Получайте доступ к полезным ресурсам, '
    'документам и справочной информации, необходимой для граждан.'
    '\n\n'
    'Мы уверены, что наш портал станет для вас надежным источником '
    'информации, а функциональные возможности облегчат взаимодействие '
    'с административной сферой города.\n'
    '\n\n'
    'Если у вас возникнут вопросы или предложения, не стесняйтесь '
    'обращаться в нашу службу поддержки.'
    '\n\n'
    'С наилучшими пожеланиями,\n'
    'Команда администрации г.Екатеринбурга.'
)


"""Email settings."""


EMAIL_HOST: str = os.getenv('EMAIL_HOST')

EMAIL_PORT: str = os.getenv('EMAIL_PORT')

EMAIL_HOST_USER: str = os.getenv('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD: str = os.getenv('EMAIL_HOST_PASSWORD')

EMAIL_USE_TLS: str = os.getenv('EMAIL_USE_TLS', False)

EMAIL_USE_SSL: str = os.getenv('EMAIL_USE_SSL', False)

EMAIL_SSL_CERTFILE: str = os.getenv('EMAIL_SSL_CERTFILE', 'None')

EMAIL_SSL_KEYFILE: str = os.getenv('EMAIL_SSL_KEYFILE', 'None')

EMAIL_TIMEOUT: int = os.getenv('EMAIL_TIMEOUT')
if EMAIL_TIMEOUT is not None:
    EMAIL_TIMEOUT: int = int(EMAIL_TIMEOUT)


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


AUTH_TOKEN: str = 'auth_token'
AUTH_JWT: str = 'auth_JWT'

CITE_DOMAIN: str = os.getenv('CITE_DOMAIN')
CITE_IP: str = os.getenv('CITE_IP')

SECRET_KEY: str = os.getenv('SECRET_KEY')

SECRET_SALT: str = os.getenv('SECRET_SALT')

PASS_ITERATIONS: int = os.getenv('PASS_ITERATIONS')
if PASS_ITERATIONS is not None:
    PASS_ITERATIONS: int = int(PASS_ITERATIONS)

USER_PASS_RAND_CYCLES: int = 3
