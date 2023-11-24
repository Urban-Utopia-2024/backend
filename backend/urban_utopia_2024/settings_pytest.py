from urban_utopia_2024.app_data import DATABASE_SQLITE
from urban_utopia_2024.settings import *  # noqa F403

DATABASES = DATABASE_SQLITE

SECRET_KEY = 'test_secret_key'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media_test')  # noqa F405
