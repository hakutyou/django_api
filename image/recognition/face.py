from api.shortcuts import Response, request_check
from external.interface import baidu_face_service, tencent_ai_service


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
    result = tencent_ai_service.face_detect(url)
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
