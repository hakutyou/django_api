from rest_framework import permissions

from api.exception import ClientError


class LoginPermission(permissions.BasePermission):
    """
    登录
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise ClientError('未登录', code=401)
        return True
