from datetime import timedelta
import os

from corsheaders.defaults import default_headers

from urban_utopia_2024.app_data import (
    AUTH_TOKEN, AUTH_JWT,
    BASE_DIR,
    DATABASE_SQLITE, DATABASE_POSTGRESQL,
    DEFAULT_FROM_EMAIL,
    EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD,
    EMAIL_USE_TLS, EMAIL_USE_SSL, EMAIL_SSL_CERTFILE,
    EMAIL_SSL_KEYFILE, EMAIL_TIMEOUT,
    CITE_DOMAIN, CITE_IP, SECRET_KEY,
)


"""App settings."""


DEBUG = True

AUTH_TYPE: str = AUTH_TOKEN


"""Celery settings."""


CELERY_BROKER_URL = 'redis://urban_utopia_2024_redis:6379/0'

CELERY_RESULT_BACKEND = 'redis://urban_utopia_2024_redis:6379/0'

CELERY_TASK_TRACK_STARTED = True

CELERY_TASK_TIME_LIMIT = 10

CELERY_TIMEZONE = 'Europe/Moscow'

CELERY_BEAT_SCHEDULE = {

}


"""Django settings."""


DATABASES = DATABASE_SQLITE if DEBUG else DATABASE_POSTGRESQL

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INSTALLED_APPS_DJANGO = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS_THIRD_PARTY = [
    'rest_framework',
    'corsheaders',
    'drf_spectacular',
    'django_celery_beat',
]

if AUTH_TYPE == AUTH_TOKEN:
    INSTALLED_APPS_THIRD_PARTY.append(
        'rest_framework.authtoken',
    )
elif AUTH_TYPE == AUTH_JWT:
    INSTALLED_APPS_THIRD_PARTY.append(
        'rest_framework_simplejwt',
    )

INSTALLED_APPS_LOCAL = [
    'api',
    'info',
    'user',
]

INSTALLED_APPS = INSTALLED_APPS_DJANGO + INSTALLED_APPS_THIRD_PARTY + INSTALLED_APPS_LOCAL

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

if AUTH_TYPE == AUTH_TOKEN:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = [
        'rest_framework.authentication.TokenAuthentication',
    ]

elif AUTH_TYPE == AUTH_JWT:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]

ROOT_URLCONF = 'urban_utopia_2024.urls'

SPECTACULAR_SETTINGS = {
    'TITLE': 'Urban Utopia 2024',
    'DESCRIPTION': 'Urbaton project',
    'VERSION': '0.0.1',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/v1/',
}

WSGI_APPLICATION = 'urban_utopia_2024.wsgi.application'


"""Email settings."""


DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL

if DEBUG:
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST: str = EMAIL_HOST

EMAIL_PORT: int = EMAIL_PORT

EMAIL_HOST_USER: str = EMAIL_HOST_USER

EMAIL_HOST_PASSWORD: str = EMAIL_HOST_PASSWORD

if EMAIL_USE_TLS == 'True':
    EMAIL_USE_TLS: bool = True
else:
    EMAIL_USE_TLS: bool = False

if EMAIL_USE_SSL == 'True':
    EMAIL_USE_SSL: bool = True
else:
    EMAIL_USE_SSL: bool = False

if EMAIL_SSL_CERTFILE == 'None':
    EMAIL_SSL_CERTFILE: None = None

if EMAIL_SSL_KEYFILE == 'None':
    EMAIL_SSL_KEYFILE: None = None

EMAIL_TIMEOUT: int = EMAIL_TIMEOUT


"""Static files settings."""


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = 'media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = 'static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


"""Regional settings."""


LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


"""Security settings."""


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

ALLOWED_HOSTS = [
    CITE_DOMAIN,
    CITE_IP,
    'localhost',
    '127.0.0.1',
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    *default_headers,
    'access-control-allow-credentials',
]

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1',
    'http://127.0.0.1:5173',
    'http://127.0.0.1:5173',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:8000',
    'http://localhost',
    'http://localhost:5173',
    'http://localhost:8000',
    f'https://{CITE_DOMAIN}',
]

CSRF_TRUSTED_ORIGINS = [
    f'https://{CITE_DOMAIN}',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SECRET_KEY = SECRET_KEY

if DEBUG:
    SIMPLE_JWT = {
        "ACCESS_TOKEN_LIFETIME": timedelta(hours=36),
    }


"""User data."""


ADMIN = 'admin'

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_USER_MODEL_USERNAME_FIELD = None

ACCOUNT_USERNAME_REQUIRED = False

AUTH_USER_MODEL = 'user.User'

USER = 'user'
