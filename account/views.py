from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.middleware import csrf
from rest_framework import exceptions, mixins
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt import views

from api.exception import ClientError
from api.shortcuts import Response
from external.interface import tencent_sms_service
from utils import xtime
from .serializer import UserSerializer, GroupSerializer


# Create your views here.
class UserView(mixins.CreateModelMixin,
               GenericAPIView):
    model = get_user_model()
    permission_classes = ()
    serializer_class = UserSerializer

    def get(self, request):
        """
        获得用户信息
        """
        # 登录校验
        if request.user.is_anonymous:
            raise ClientError('未登录', code=401)
        data = {
            'username': request.user.username,
            'last_login': xtime.to_strtime(request.user.last_login),
        }
        return Response(request, 0, data=data)

    def post(self, request, *args, **kwargs):
        """
        注册新用户
        """
        # 验证码校验
        code = request.POST.get('code')
        mobile = request.POST.get('mobile')
        if (not code) or (not mobile):
            raise ClientError('手机或验证码未填写', code=400)
        if not tencent_sms_service.check_sms('register', mobile, code):
            raise ClientError('短信验证码错误', code=401)
        # 创建用户
        return self.create(request, *args, **kwargs)


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
class GroupView(mixins.CreateModelMixin,
                GenericAPIView):
    """
    用户组
    """
    model = Group
    serializer_class = GroupSerializer
