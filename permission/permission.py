from rest_framework import permissions

from api.exception import ClientError
from external.interface import tencent_sms_service


class LoginPermission(permissions.BasePermission):
    """
    登录
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise ClientError('未登录', code=401)
        return True


class UserPermission(LoginPermission):
    """
    注册手机相关
    """

    def has_permission(self, request, view):
        # 注册新用户需要校验短信验证码
        if request.method == 'POST':
            code = request.POST.get('code')
            mobile = request.POST.get('mobile')
            if (not code) or (not mobile):
                raise ClientError('手机或验证码未填写', code=400)
            if not tencent_sms_service.check_sms('register', mobile, code):
                raise ClientError('短信验证码错误', code=401)
            return True
        return super().has_permission(request, view)
