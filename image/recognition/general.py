from api.exception import ClientError
from api.shortcuts import Response, request_check
from external.interface import vision_service


@request_check(
    url=(str, True),
)
def general_recognition(request):
    url = request.post.get('url')
    try:
        result = vision_service.image_detect(url)
    except KeyError:
        raise ClientError('图片格式错误')
    return Response(request, 0, data=result)
