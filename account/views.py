from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.middleware import csrf
from rest_framework import generics, exceptions
from rest_framework_simplejwt import views

import utils
from api.exception import ClientError
from api.shortcuts import Response
from permission import permission
from .serializer import UserSerializer, GroupSerializer


# Create your views here.
class UserView(generics.CreateAPIView):
    """
    新建用户在 UserSerializer 实现
    获得用户信息通过 get
    """
    model = get_user_model()
    permission_classes = (permission.UserPermission,)
    serializer_class = UserSerializer

    def get(self, request):
        data = {
            'username': request.user.username,
            'last_login': utils.get_time(request.user.last_login),
        }
        return Response(request, 0, data=data)


user_view = UserView.as_view()


class LoginView(views.TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        except exceptions.AuthenticationFailed:
            raise ClientError('用户名或密码错误', code=401)
        token = csrf.get_token(request)
        response.data['csrf_token'] = token
        UserSerializer.login(request.POST['username'])
        return response


login_view = LoginView.as_view()


# TODO: 权限功能
class GroupView(generics.CreateAPIView):
    """
    用户组
    """
    model = Group
    serializer_class = GroupSerializer
