from django.contrib.auth import get_user_model
from rest_framework.decorators import permission_classes, api_view

from api.shortcuts import Response
from external.interface import tencent_sms_service
from permission import permission

UserModel = get_user_model()


def reset_password(request):
    username = request.POST.get('username')
    mobile = request.POST.get('mobile')
    new_password = request.POST.get('new_password')
    code = request.POST.get('code')
    if not (username and mobile and code and new_password):
        return Response(2)

    try:
        user = UserModel.objects.get(username=username, mobile=mobile, is_active=1)
    except UserModel.DoesNotExist:
        return Response(202)

    if not tencent_sms_service.check_sms('reset_password', mobile, code):
        return Response(201)

    user.set_password(new_password)
    user.save()
    return Response(0)


@api_view(['POST'])
@permission_classes((permission.LoginPermission,))
def modify_password(request):
    password = request.POST.get('password')
    new_password = request.POST.get('new_password')
    if not (password and new_password):
        return Response(2, convert=True)

    if not request.user.check_password(password):
        return Response(211, convert=True)

    request.user.set_password(new_password)
    request.user.save()
    return Response(0, convert=True)
