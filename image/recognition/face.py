from api.shortcuts import Response
from external.interface import baidu_face_service


def face_detect(request):
    try:
        url = request.POST['url']
        field = request.POST.get('field', '')
    except KeyError:
        return Response(2)

    result = baidu_face_service.face_detect(url, field)
    return Response(0, data=result)
