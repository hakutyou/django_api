import json
import traceback

import redis
import time
from django.conf import settings
from log_request_id.session import Session

from api.exception import ClientError, ServiceError
from api.service import logger
from api.shortcuts import Response
from external.interface.mail import internal_send_mail
from utils import protect_dict_or_list, xtime


class EnhanceMiddleware(object):
    def __init__(self, get_response):
        self.mail_time = time.time()  # 上次发送邮件的时间
        self.get_response = get_response

    def __call__(self, request):
        # Request
        request.time_begin = xtime.now()
        request_post = request.POST or request.body

        # 接收到请求
        if isinstance(request_post, dict):
            request_post = json.dumps(protect_dict_or_list(request_post), indent=2, sort_keys=True, ensure_ascii=False)
        logger.info('response_accept', extra={
            'uri': f'{request.scheme}://{request.get_host()}{request.get_full_path()}',
            'remote_ip': request.META.get('REMOTE_ADDR'),
            'authorization': request.META.get('HTTP_AUTHORIZATION'),
            # postman 需要传入 header 参数为 internal-token（去掉前面的 HTTP- 并且使用减号代替下划线）
            'internal_token': request.META.get('HTTP_INTERNAL_TOKEN'),
            'method': request.method,
            'data': request_post,
        })
        request.do_request = Session()
        response = self.get_response(request)
        # 返回请求的日志在 shortcuts.py 中
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
