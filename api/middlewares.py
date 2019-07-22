import time
import traceback

import redis
from django.conf import settings
from django.core import mail
from django.http import HttpResponse, JsonResponse

from api.settings import DEBUG
from api.shortcuts import Response, logger


class EnhanceMiddleware(object):
    def __init__(self, get_response):
        self.mail_time = time.time()  # 上次发送邮件的时间
        self.get_response = get_response

    def __call__(self, request):
        # before get_response
        time_begin = time.time()
        response = self.get_response(request)
        time_cost = time.time() - time_begin
        # after get_response
        # receive_time = datetime.fromtimestamp(time_begin).strftime('%Y-%m-%d %H:%M:%S')
        logger.info({
            'cost_time': time_cost,
            'request': {
                'scheme': request.scheme,
                'path': request.path,
                'encoding': request.encoding,
                # 'session': request.session,
                'COOKIES': request.COOKIES,
                'method': request.method,
                'POST': request.POST,
                'GET': request.GET,
            },
            'response': response,
        })
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

    if DEBUG:
        logger.info('【Error】\n'
                    f'{exception}: {traceback.format_exc()}')
    elif time.time() - self.mail_time > 60:
        # 60s 只发送一次
        mail.send_mail(exception, traceback.format_exc(),
                       settings.EMAIL_HOST_USER, settings.EMAIL_MANAGER)
        self.mail_time = time.time()
        return Response(1001)

    return Response(1000)
