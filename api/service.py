import logging

# Logger
logger = logging.getLogger(__name__)

# Celery
from django.conf import settings
from celery import Celery

app = Celery('my_task', broker=settings.CELERY_BROKER, backend=settings.CELERY_BACKEND)
