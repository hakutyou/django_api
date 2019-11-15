import rest_framework.serializers
from django.contrib.auth import get_user_model

from utils import xtime

UserModel = get_user_model()


class UserSerializer(rest_framework.serializers.ModelSerializer):
    password = rest_framework.serializers.CharField(write_only=True)

    # 给 serializer_class 使用
    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            mobile=validated_data['mobile']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    # 直接调用
    @staticmethod
    def login(user):
        user.last_login = xtime.now()
        user.save(update_fields=['last_login'])
        return

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'email', 'password', 'mobile')


class GroupSerializer(rest_framework.serializers.ModelSerializer):
    # TODO: 权限功能
    pass
