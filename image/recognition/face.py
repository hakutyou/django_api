from api.shortcuts import Response, request_check
from external.interface import baidu_face_service


@request_check(
    url=(str, True),
    field=(str, False),
)
def face_detect(request):
    url = request.post.get('url')
    field = request.post.get('field', '')
    result = baidu_face_service.face_detect(url, field)
    return Response(request, 0, data=result)
