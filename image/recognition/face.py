from api.shortcuts import Response, request_check
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
def face_add(request):
    url = request.post.get('url')
    person_name = request.post.get('name')
    # 检测是否存在
    try:
        result = tencent_face_service.face_idperson(url=url)['data']['candidates'][0]['confidence']
        if result > 80:
            return Response(request, 1, msg='人脸已经存在')
    except (IndexError, KeyError):
        pass
    # 录入
    result = tencent_face_service.face_newperson(url=url, person_name=person_name)
    return Response(request, 0, data=result)


@request_check(
    person_id=(str, True),
)
def face_del(request):
    person_id = request.post.get('person_id')
    try:
        result = tencent_face_service.face_delperson(person_id=person_id)
    except FaceUser.DoesNotExist:
        return Response(request, 1, msg='不存在该用户')
    return Response(request, 0, data=result)


@request_check(
    url=(str, True)
)
def face_identify(request):
    url = request.post.get('url')
    result = tencent_face_service.face_idperson(url=url)
    return Response(request, 0, data=result)


def face_list(request):
    result = tencent_face_service.face_listperson()
    return Response(request, 0, data=result)
