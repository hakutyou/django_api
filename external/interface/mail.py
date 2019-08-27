from django.conf import settings
from django.core import mail
from rest_framework.decorators import permission_classes, api_view

from api.exception import ServiceError
from api.service import app
from api.shortcuts import Response
from permission import permission
from utils import get_time, now, random_string
from utils.celery import celery_stage, celery_catch


@app.task(bind=True)
@celery_catch
def celery_send_mail(self, subject, message, receive):
    mail.send_mail(subject, message,
                   settings.EMAIL_HOST_USER, receive)


@api_view(['POST'])
@permission_classes((permission.LoginPermission,))
def send_mail(request):
    subject = request.POST.get('subject')
    message = request.POST.get('message')
    receive = request.POST.get('receive')
    if not (subject and message and receive):
        raise ServiceError('Argument Error', code=400)
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
