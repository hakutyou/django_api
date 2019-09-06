from api.shortcuts import Response, request_check
from external.interface import face_service
from image.models import FaceUser


@request_check(
    url=(str, True),
    # field=(str, False),
)
def face_detect(request):
    url = request.post.get('url')
    # field = request.post.get('field', '')
    result = face_service.face_detect(url)
    return Response(request, 0, data=result)


@request_check(
    url=(str, True),
    # field=(str, False),
)
def face_verify(request):
    url = request.post.get('url')
    # field = request.post.get('field', '')
    result = face_service.face_verify(url)
    return Response(request, 0, data=result)


@request_check(
    url_1=(str, True),
    url_2=(str, True),
)
def face_compare(request):
    url_1 = request.post.get('url_1')
    url_2 = request.post.get('url_2')
    result = face_service.face_compare(url_1, url_2)
    return Response(request, 0, data=result)


@request_check(
    url=(str, True),
    user_name=(str, True),
)
def user_add(request):
    url = request.post.get('url')
    user_name = request.post.get('user_name')
    # 录入
    result = face_service.user_add(url=url, user_name=user_name)
    return Response(request, 0, data=result)


@request_check(
    user_id=(str, True),
)
def user_remove(request):
    user_id = request.post.get('user_id')
    try:
        result = face_service.user_remove(user_id)
    except FaceUser.DoesNotExist:
        return Response(request, 1, msg='不存在该用户')
    return Response(request, 0, data=result)


@request_check(
    url=(str, True)
)
def user_search(request):
    url = request.post.get('url')
    result = face_service.user_search(url=url)
    return Response(request, 0, data=result)


def user_list(request):
    result = face_service.user_list()
    return Response(request, 0, data=result)
