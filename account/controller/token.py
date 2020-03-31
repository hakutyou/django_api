import time
from django.conf import settings
from django.core.cache import cache

from api.exception import ServiceError, ClientError
from api.shortcuts import Response
from utils import xcrypt


def require_internal_auth(func):
    def get_token(data: dict) -> str:
        # 传入 random_str
        # 前 10 位为 time.time(), 计算后的 1 分钟内有效, 仅能使用一次
        # f'{int(time.time()):010}{random_string()}'
        try:
            random_str = data.get('random_str')
            request_time = int(random_str[:10])
        except (ValueError, TypeError):
            raise ServiceError('random_str format error', code=401)
        if not request_time:
            raise ServiceError('expected random_str', code=400)
        if time.time() - request_time > 60:
            raise ClientError('请求超时', code=401)
        if cache.get(f'token:{random_str}'):
            raise ClientError('请勿重复请求', code=401)
        cache.set(f'token:{random_str}', 1, 60 + 10)
        split_joint = ''
        for i in data:
            split_joint += str(i)
            split_joint += str(data[i])
        # 末尾添加 secret_key
        split_joint += 'secret_key' + settings.SECRET_KEY
        print(split_joint)
        return xcrypt.message_digest(split_joint)

    def wrapper(request, *args, **kwargs):
        if request.META.get('HTTP_INTERNAL_TOKEN') != get_token(request.POST.dict()):
            return Response(-1)
        return func(request, *args, **kwargs)

    return wrapper
