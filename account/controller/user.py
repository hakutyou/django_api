from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.decorators import permission_classes, api_view

from api.exception import ClientError
from api.shortcuts import Response, request_check
from external.interface import tencent_sms_service
from permission import permission
from utils import captcha, random_string

UserModel = get_user_model()


@request_check(
    username=(str, True),
    mobile=(int, True),
    code=(str, True),
    new_password=(str, True)
)
def reset_password(request):
    username = request.post.get('username')
    mobile = request.post.get('mobile')
    new_password = request.post.get('new_password')
    code = request.post.get('code')
    try:
        user = UserModel.objects.get(username=username, mobile=mobile, is_active=1)
    except UserModel.DoesNotExist:
        raise ClientError('账号不存在或手机错误', code=401)

    if not tencent_sms_service.check_sms('reset_password', mobile, code):
        raise ClientError('验证码错误', code=401)

    user.set_password(new_password)
    user.save(update_fields=['password'])
    return Response(request, 0)


@api_view(['POST'])
@permission_classes((permission.LoginPermission,))
@request_check(
    password=(str, True),
    new_password=(str, True),
)
def modify_password(request):
    password = request.post.get('password')
    new_password = request.post.get('new_password')
    if not request.user.check_password(password):
        raise ClientError('原密码错误', code=401)

    request.user.set_password(new_password)
    request.user.save(update_fields=['password'])
    return Response(request, 0)


@request_check(
    b64=(int, False),
    sign=(str, True),
)
def get_captcha(request):
    """
    最简单的图片验证码
    """
    b64 = request.post.get('b64', 0)
    # 通过签名区分不同客户端请求
    sign = request.post.get('sign')

    # 防止混淆
    exclude = '0129'  # 0:O, 1:l, 2:z, 9:g
    code = random_string(length=4, exclude=exclude)
    print(code)
    cache.set(f'captcha:{sign}', code.lower(), 60 + 10)
    if b64 == 0:
        response_text = captcha.get_captcha_base64(code)
        return Response(request, 0, _type='gif', data=response_text)
    response_text = f'data:image/png;base64,{captcha.get_captcha_base64("1234", b64=True).decode()}'
    return Response(request, 0, _type='str', data=response_text)


@request_check(
    sign=(str, True),
    code=(str, True),
)
def check_captcha(request):
    """
    验证验证码正确性，单独调用可能会通过修改 html 跳过这个步骤
    应该放在 login 内，如果验证码错误就不返回 access_token
    """
    sign = request.post.get('sign')
    code = request.post.get('code').lower()
    right_code = cache.get(f'captcha:{sign}')
    if right_code is None:
        raise ClientError('验证码超时，请刷新重试')
    if right_code != code:
        cache.delete(f'captcha:{sign}')
        raise ClientError('验证码错误')
    return Response(request, 0)
