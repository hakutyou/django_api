from api.shortcuts import Response
from external.interface import tencent_sms_service


def sms_sender(request):
    mobile = request.POST.get('mobile')
    if not mobile:
        return Response(200)
    tencent_sms_service.send_sms('注册', mobile)
    return Response(0)
