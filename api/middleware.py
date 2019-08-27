import traceback

import redis
import time
from django.conf import settings

from api.exception import ClientError, ServiceError
from api.shortcuts import Response
from external.interface.mail import internal_send_mail


class EnhanceMiddleware(object):
    def __init__(self, get_response):
        self.mail_time = time.time()  # 上次发送邮件的时间
        self.get_response = get_response

    def __call__(self, request):
        # Request
        request.time_begin = time.time()
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        _exception_code = {
            redis.exceptions.ConnectionError: lambda: {
                'code': -1,
                'msg': 'Redis Error',
            },
            ClientError: lambda: {
                'code': exception.code,
                'msg': exception.response,
            },
            ServiceError: lambda: {
                'code': exception.code,
                'msg': exception.response,
            },
        }

        error_info = _exception_code.get(type(exception))
        if error_info:
            error_info = error_info()
            return Response(request, code=error_info['code'], msg=error_info['msg'])

        if settings.DEBUG or (time.time() - self.mail_time < 60):
            code = 1000
        else:
            code = 1001
            internal_send_mail(exception, traceback.format_exc(),
                               settings.EMAIL_RECEIVER)
            self.mail_time = time.time()
        return Response(request, code=code, exception=exception, traceback=traceback.format_exc())
