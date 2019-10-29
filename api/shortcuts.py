import types

import time
from django.http import JsonResponse, HttpResponse

from api.exception import ServiceError
from api.service import logger


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
    status = _status_mapper.get(code, 400)
    # logger
    time_cost = time.time() - request.time_begin

    if code == 0:
        logger.info('ok', extra={
            'uri': f'{request.scheme}://{request.get_host()}{request.get_full_path()}',
            'rid': request.rid,
            'koto': 'response_return',
            'duration': str(time_cost),
            'method': request.method,
            'response': str(ret),
        })
    elif code >= 1000:
        logger.error('error', extra={
            'uri': f'{request.scheme}://{request.get_host()}{request.get_full_path()}',
            'rid': request.rid,
            'level': 'error',
            'koto': 'response_error',
            'method': request.method,
            'response': f'{kwargs["exception"]}\n{kwargs["traceback"]}',
        })
    else:
        logger.warning('warning', extra={
            'uri': f'{request.scheme}://{request.get_host()}{request.get_full_path()}',
            'rid': request.rid,
            'level': 'warning',
            'koto': 'response_warning',
            'method': request.method,
            'response': str(ret),
        })
    return _type_mapper[_type](ret, status=status, content_type=content_type)


def request_check(**check_kwargs):
    """
    @request_check({
        id=[int, True],
        amount=[int, False],
    })
    ------------------------
    request.POST['id'] -> int, MUST
    request.POST['amount'] -> int, Option
    """

    def _request_check(func):
        def wrapper(request, *args, **kwargs):
            request_method_mapper = {
                'POST': lambda: request.POST,
                'GET': lambda: request.GET,
            }
            request_method = request_method_mapper.get(request.method)
            if not request_method:
                return ServiceError('Expect method Error')
            request_data = request_method()
            request.post = {}
            for i in check_kwargs:
                real_i = request_data.get(i, None)
                need_type = check_kwargs[i][0]
                is_option = check_kwargs[i][1]
                if not real_i:  # without this argument
                    if is_option is False:  # allow
                        continue
                    raise ServiceError('Argument Error', code=400)
                else:  # have this argument
                    if type(need_type) in [type, types.FunctionType]:
                        try:
                            request.post[i] = need_type(real_i)
                        except Exception:
                            raise ServiceError('Argument Error', code=400)
                        continue
                    raise ServiceError('Expect method Error', code=400)
            return func(request, *args, **kwargs)

        return wrapper

    return _request_check
