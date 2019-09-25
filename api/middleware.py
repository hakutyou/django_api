import traceback

import redis
import time
from django.conf import settings

from api.exception import ClientError, ServiceError
from api.service import logger
from api.shortcuts import Response
from external.interface.mail import internal_send_mail
from utils import random_string


class EnhanceMiddleware(object):
    def __init__(self, get_response):
        self.mail_time = time.time()  # 上次发送邮件的时间
        self.get_response = get_response

    def __call__(self, request, time_time=time.time()):
        # Request
        request.time_begin = time_time
        request_post = request.POST or request.body
        request.rid = f'{request.time_begin}{random_string()}'
        logger.info(request_post, extra={
            'uri': f'{request.scheme}://{request.get_host()}{request.get_full_path()}',
            'rid': request.rid,
            'remote_ip': request.META.get('REMOTE_ADDR'),
            'authorization': request.META.get('HTTP_AUTHORIZATION'),
            # postman 需要传入 header 参数为 internal-token（去掉前面的 HTTP- 并且使用减号代替下划线）
            'internal_token': request.META.get('HTTP_INTERNAL_TOKEN'),
            'koto': 'response_accept',
            'method': request.method,
        })
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
