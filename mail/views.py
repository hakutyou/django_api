from django.conf import settings
from django.core import mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from api.shortcuts import Response


# Create your views here.
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def send_mail(request):
    subject = request.data.get('subject')
    message = request.data.get('message')
    mail.send_mail(subject, message,
                   settings.EMAIL_HOST_USER, [request.data.get('receive')])
    return Response(0)
