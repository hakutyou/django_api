from django.conf import settings
from django.core import mail
from rest_framework.decorators import permission_classes, api_view

from api.service import app
from api.shortcuts import Response, request_check
from permission import permission
from utils.celery import celery_stage, celery_catch
from utils.utils import random_string
from utils.xtime import get_time, now


@app.task(bind=True)
@celery_catch
def celery_send_mail(self, subject, message, receive):
    mail.send_mail(subject, message,
                   settings.EMAIL_HOST_USER, receive)


@api_view(['POST'])
@permission_classes((permission.LoginPermission,))
@request_check(
    subject=(str, True),
    message=(str, True),
    receive=(str, True),
)
def send_mail(request):
    subject = request.post.get('subject')
    message = request.post.get('message')
    receive = request.post.get('receive')
    internal_send_mail(subject, message, [receive])
    return Response(request, 0)


# 给 api 内部调用
def internal_send_mail(subject, message, receive):
    _type = 'mail'
    ic = get_time(now(), time_format='%Y%m%d%H%M%S') + random_string(length=6)
    celery_stage(ic, _type, 0)
    celery_send_mail.delay(ic, _type, subject, message, receive)
    # print(celery_send_mail)
    return
