from rest_framework import permissions


class LoginPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.id is not None:  # AnonymousUser.id == None
            return True
        return False


class UserPermission(LoginPermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super().has_permission(request, view)
