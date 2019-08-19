from django.http import JsonResponse
from rest_framework import response

_ERROR_LIST = {
    # 小于 0 为 外部错误
    -1: 'Qcloud Error',  # 腾讯云 Cos 错误
    -2: 'Redis Error',  # Redis 错误
    # 大于 0 为 内部错误
    1: 'Return Error',  # 返回类型错误
    2: 'Argument Error',  # 参数错误
    3: 'Permission Denied',
    4: 'Request Denied',  # 请求方式(POST, GET)错误
    # 3: 'Not Found Error',
    # 4: 'Require Login',
    # 100 到 199 为自定义错误
    # 200 到 299 为用户错误
    200: '请输入手机号码',
    201: '短信验证码错误',
    202: '账号不存在或手机错误',
    210: '请先登录',
    211: '原密码错误',
    270: '记录不存在',
    280: '人脸检测失败',
    # 其他错误
    999: 'TODO',  # 留坑待完善
    1000: 'Fatal Error',  # 未捕捉的错误
    1001: 'Fatal Error',  # 未捕捉的错误, 发送邮件
}


# noinspection PyPep8Naming
def Response(code, msg='', data=None, view=False, convert=False):
    ret = {'code': code}
    if code != 0:  # 出现错误
        if code in _ERROR_LIST.keys():
            ret['msg'] = _ERROR_LIST[code]
        else:
            assert (100 <= code < 200)  # 只有 100 到 199 为自定义错误
            ret['msg'] = msg
    if data is not None:
        ret['data'] = data
    if view:  # TODO: view 先返回 Response 数据
        ret = response.Response(ret)
    if convert:
        ret = JsonResponse(ret)
    return ret


# key, type
def check_request(keys):
    """
    装饰器, 用于检查 requests 的参数
    用法示例
    @check_request({
        'name': [char]
        'age': [int, None]
    })
    def create_user(request):
        ....
    """

    def _check_request(func):
        def wrapper(request, *args, **kwargs):
            request.post = {}
            for key in keys:
                ap = request.POST.get(key, None)  # 实参
                if type(ap) not in keys[key]:
                    return Response(2)
            return func(request, *args, **kwargs)

        return wrapper

    return _check_request
