from rest_framework import permissions
from rest_framework.exceptions import APIException

from api.shortcuts import Response
from external.interface import tencent_sms_service


class LoginPermission(permissions.BasePermission):
    """
    登录
    """

    def has_permission(self, request, view):
        if request.user.id is not None:  # AnonymousUser.id == None
            return True
        APIException.default_detail = Response(210)
        raise APIException


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
                APIException.default_detail = Response(200)
                raise APIException
            if not tencent_sms_service.check_sms('注册', mobile, code):
                APIException.default_detail = Response(201)
                raise APIException
            return True
        return super().has_permission(request, view)
