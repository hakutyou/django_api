import json
import traceback

import redis
import time
from django.conf import settings
from django.http import HttpResponse, JsonResponse

from api.service import logger
from api.shortcuts import Response
from external.interface.mail import internal_send_mail
from utils import string_color, protect_dict


class EnhanceMiddleware(object):
    def __init__(self, get_response):
        self.mail_time = time.time()  # 上次发送邮件的时间
        self.get_response = get_response

    def __call__(self, request):
        # Request
        time_begin = time.time()
        response = self.get_response(request)
        time_cost = time.time() - time_begin

        # Logger
        data = None
        if request.method == 'POST':
            try:
                data = request.POST.dict()
            except AttributeError:
                data = request.body
        try:
            result = response.data
        except AttributeError:
            result = response

        if type(data) == dict:
            data = json.dumps(protect_dict(data), indent=4, ensure_ascii=False)
        if type(result) == dict:
            result = json.dumps(protect_dict(result), indent=4, ensure_ascii=False)

        logger.info(f'{request.scheme}://{request.get_host()}{request.get_full_path()}',
                    extra={
                        'koto': 'response',
                        'duration': str(time_cost),
                        # 'receive_time': datetime.fromtimestamp(time_begin).strftime('%Y-%m-%d %H:%M:%S')
                        'method': request.method,
                        # 'get': dict(request.GET),
                        'data': string_color(data, 'green'),
                        # 'cookies': request.COOKIES,
                        'response': string_color(result, 'pink'),
                    })

        # Response
        if type(response) == dict:
            response = JsonResponse(response)
        elif type(response) == str:
            response = HttpResponse(response)
        return response

    def process_exception(self, request, exception):
        _exception_type = {
            redis.exceptions.ConnectionError: -2
        }
        response = _exception_type.get(type(exception))
        if response:
            return Response(response)

        data = None
        if request.method == 'POST':
            try:
                data = json.dumps(request.POST.dict(), indent=4, ensure_ascii=False)
            except AttributeError:
                data = request.body

        if type(data) == dict:
            data = json.dumps(protect_dict(data), indent=4, ensure_ascii=False)

        logger.error(f'{request.scheme}://{request.get_host()}{request.get_full_path()}',
                     extra={
                         'method': request.method,
                         # 'get': dict(request.GET),
                         'data': string_color(data, 'yellow'),
                         'expect': string_color(f'{exception}: {traceback.format_exc()}', 'red')
                         # 'cookies': request.COOKIES,
                     })
        if settings.DEBUG or (time.time() - self.mail_time < 60):
            return Response(1000)
        # 正式环境 60s 只发送一次
        internal_send_mail(exception, traceback.format_exc(),
                           settings.EMAIL_RECEIVER)
        self.mail_time = time.time()
        return Response(1001)
