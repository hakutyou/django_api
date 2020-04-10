import json
import types

from django.http import JsonResponse, HttpResponse

from api.exception import ServiceError
from api.celery import logger
# noinspection PyPep8Naming
from utils import protect_dict_or_list, xtime


def Response(request, code=0, _type='dict', **kwargs):
    """
    code == 0 表示正常的返回
    code > 0 表示错误的 request
        code == 401 表示认证错误(401)
    code < 0 表示外部错误
    """
    _status_mapper = {
        0: 200,
        204: 204,  # 删除成功
        400: 400,  # 参数有误
        401: 401,  # 认证失败
        500: 500,  # 未曾预料的请求
    }
    _type_mapper = {
        'dict': JsonResponse,
    }
    _content_type = {
        'gif': 'image/gif',
        'str': 'text/plain',
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
        content_type = kwargs.get('content_type', _content_type.get(_type, 'text/plain'))
    status = _status_mapper.get(code, 400)
    # logger
    time_cost = xtime.now() - request.time_begin

    if isinstance(ret, dict):
        pretty_ret = json.dumps(protect_dict_or_list(ret), indent=2, sort_keys=True, ensure_ascii=False)
    else:
        pretty_ret = str(ret)

    if code == 0:
        logger.info('response_return', extra={
            'uri': f'{request.scheme}://{request.get_host()}{request.get_full_path()}',
            'duration': str(time_cost.total_seconds()),
            'method': request.method,
            'response': pretty_ret,
        })
    elif code >= 1000:
        logger.error('response_error', extra={
            'uri': f'{request.scheme}://{request.get_host()}{request.get_full_path()}',
            'level': 'error',
            'duration': str(time_cost.total_seconds()),
            'method': request.method,
            'response': f'{kwargs["exception"]}\n{kwargs["traceback"]}',
        })
    else:
        logger.warning('response_warning', extra={
            'uri': f'{request.scheme}://{request.get_host()}{request.get_full_path()}',
            'level': 'warning',
            'duration': str(time_cost.total_seconds()),
            'method': request.method,
            'response': pretty_ret,
        })
    _response = _type_mapper.get(_type, HttpResponse)
    return _response(ret, status=status, content_type=content_type)


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
