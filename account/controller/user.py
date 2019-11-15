from django.contrib.auth import get_user_model
from rest_framework.decorators import permission_classes, api_view

from api.exception import ClientError
from api.shortcuts import Response, request_check
from external.interface import tencent_sms_service
from permission import permission

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
