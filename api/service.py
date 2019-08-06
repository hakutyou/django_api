import logging
import os

from celery import Celery
from django.conf import settings

# Logger
logger = logging.getLogger(__name__)

# Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
app = Celery('api', broker=settings.CELERY_BROKER, backend=settings.CELERY_BACKEND)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
