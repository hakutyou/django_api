from api.exception import ServiceError
from api.shortcuts import Response
from external.interface import baidu_face_service


def face_detect(request):
    try:
        url = request.POST['url']
        field = request.POST.get('field', '')
    except KeyError:
        raise ServiceError('Argument Error', code=400)

    result = baidu_face_service.face_detect(url, field)
    return Response(request, 0, data=result)
