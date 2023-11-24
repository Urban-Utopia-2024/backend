import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urban_utopia_2024.settings')

app = Celery('urban_utopia_2024')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
