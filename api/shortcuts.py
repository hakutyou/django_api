import time
from django.http import JsonResponse, HttpResponse

from api.service import logger
from utils import string_color


# noinspection PyPep8Naming
def Response(request, code=0, _type='dict', **kwargs):
    """
    code == 0 表示正常的返回
    code > 0 表示错误的 request
        code == 401 表示认证错误(401)
    code < 0 表示外部错误
    """
    _status_mapper = {
        0: 200,
        400: 400,  # 参数有误
        401: 401,  # 认证失败
        500: 500,  # 未曾预料的请求
    }
    _type_mapper = {
        'dict': JsonResponse,
        'str': HttpResponse,
    }
    if _type == 'dict':
        if code < 1000:
            ret = kwargs
        else:
            ret = {}
        ret['code'] = code
        content_type = 'application/json'
    else:
        ret = kwargs.get('data', '')
        content_type = kwargs.get('content_type', 'text/plain')
    status = _status_mapper.get(code, 500)
    # logger
    time_cost = time.time() - request.time_begin
    if code == 0:
        logger.info(f'{request.scheme}://{request.get_host()}{request.get_full_path()}',
                    extra={
                        'koto': 'response',
                        'duration': str(time_cost),
                        'method': request.method,
                        'request': string_color(request.POST, 'green'),
                        'response': string_color(ret, 'pink'),
                    })
    elif code >= 1000:
        logger.error(f'{request.scheme}://{request.get_host()}{request.get_full_path()}',
                     extra={
                         'method': request.method,
                         'request': string_color(request.POST, 'yellow'),
                         'response': string_color(f'{kwargs["exception"]}\n{kwargs["traceback"]}', 'red')
                     })
    else:
        logger.warning(f'{request.scheme}://{request.get_host()}{request.get_full_path()}',
                       extra={
                           'method': request.method,
                           'request': string_color(request.POST, 'cyan'),
                           'response': string_color(f'{ret}', 'yellow')
                       })
    return _type_mapper[_type](ret, status=status, content_type=content_type)
