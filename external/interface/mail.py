from rest_framework.decorators import permission_classes, api_view

from api.shortcuts import Response, request_check
from external.celery.tasks import send_mail_celery
from permission import permission
from utils.celery import append_celery


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
    # 加入 celery 队列
    append_celery('mail', send_mail_celery, subject, message, [receive])
    return Response(request, 0)
