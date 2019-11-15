from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.middleware import csrf
from rest_framework import generics, exceptions
from rest_framework_simplejwt import views

from api.exception import ClientError
from api.shortcuts import Response
from permission import permission
from utils import xtime
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
            'last_login': xtime.to_strtime(request.user.last_login),
        }
        return Response(request, 0, data=data)


user_view = UserView.as_view()


class LoginView(views.TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context=self.get_serializer_context())
            serializer.is_valid(raise_exception=True)
        except exceptions.AuthenticationFailed:
            raise ClientError('用户名或密码错误', code=401)
        token = csrf.get_token(request)
        serializer.validated_data['csrf_token'] = token
        UserSerializer.login(serializer.user)
        # 内部调用使用 request.do_request 代替 requests 以保持 rid 一致
        # request.do_request.get('http://127.0.0.1:8000/account/user/')
        return Response(request, 0, **serializer.validated_data)


login_view = LoginView.as_view()


# TODO: 权限功能
class GroupView(generics.CreateAPIView):
    """
    用户组
    """
    model = Group
    serializer_class = GroupSerializer
