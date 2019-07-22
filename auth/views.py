from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import generics
from rest_framework_simplejwt import views

import utils
from api.shortcuts import Response
from .permission import permission
from .serializer import UserSerializer, GroupSerializer


# Create your views here.
class UserView(generics.CreateAPIView):
    """
    新建用户
    """
    model = get_user_model()
    permission_classes = (permission.UserPermission,)
    serializer_class = UserSerializer

    def get(self, request):
        data = {
            'username': request.user.username,
            'last_login': utils.get_time(request.user.last_login),
        }
        return Response(0, data=data, view=True)


user_view = UserView.as_view()


class GroupView(generics.CreateAPIView):
    """
    用户组
    """
    model = Group
    serializer_class = GroupSerializer


class LoginView(views.TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        UserSerializer.login(request.POST['username'])
        return response


login_view = LoginView.as_view()
