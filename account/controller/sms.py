from api.exception import ClientError
from api.shortcuts import Response
from external.interface import tencent_sms_service

ACTION_RANGE = [
    'register',
    'reset_password',
]


def sms_sender(action):
    def _sms_sender(request):
        mobile = request.POST.get('mobile')
        if (not mobile) or (action not in ACTION_RANGE):
            return ClientError('请输入手机号码', code=400)
        tencent_sms_service.send_sms(action, mobile)
        return Response(request, 0)

    return _sms_sender
