from django.conf import settings
from django.core import mail
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from api.service import app
from api.shortcuts import Response
from utils import get_time, now, random_string
from utils.celery import celery_stage, celery_catch
from utils.limit import API_METHOD


@app.task(bind=True)
@celery_catch
def celery_send_mail(self, post):
    subject = post.get('subject')
    message = post.get('message')
    mail.send_mail(subject, message,
                   settings.EMAIL_HOST_USER, [post.get('receive')])


@permission_classes((IsAuthenticated,))
@API_METHOD('POST')
def send_mail(request):
    _type = 'mail'
    ic = get_time(now(), format='%Y%m%d%H%M%S') + random_string(length=6)
    celery_stage(ic, _type, 0)
    celery_send_mail.delay(ic, _type, request.POST)
    print(celery_send_mail)
    return Response(0)
