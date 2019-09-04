from api.shortcuts import Response, request_check
from external.abstract import face_service
from external.interface import baidu_face_service, tencent_face_service
from image.models import FaceUser


@request_check(
    url=(str, True),
    field=(str, False),
)
def face_detect(request):
    url = request.post.get('url')
    field = request.post.get('field', '')
    result = baidu_face_service.face_detect(url, field)
    return Response(request, 0, data=result)


@request_check(
    url=(str, True),
)
def tencent_face_detect(request):
    url = request.post.get('url')
    result = tencent_face_service.face_detect(url)
    return Response(request, 0, data=result)


@request_check(
    url=(str, True),
    field=(str, False),
)
def face_verify(request):
    url = request.post.get('url')
    field = request.post.get('field', '')
    result = baidu_face_service.face_verify(url, field)
    return Response(request, 0, data=result)


@request_check(
    url_1=(str, True),
    url_2=(str, True),
)
def face_compare(request):
    url_1 = request.post.get('url_1')
    url_2 = request.post.get('url_2')
    result = baidu_face_service.face_compare(url_1, url_2)
    return Response(request, 0, data=result)


@request_check(
    url=(str, True),
    name=(str, True),
)
def user_add(request):
    url = request.post.get('url')
    person_name = request.post.get('name')
    # 录入
    result = face_service.user_add(url=url, person_name=person_name)
    return Response(request, 0, data=result)


@request_check(
    user_id=(str, True),
)
def face_del(request):
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


def face_list(request):
    result = tencent_face_service.face_listperson()
    return Response(request, 0, data=result)
