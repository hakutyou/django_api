from api.shortcuts import Response
from external.package import baidu


def face_detect(request):
    try:
        url = request.POST['url']
    except KeyError:
        return Response(2)

    result = baidu.face_detect(url)
    return Response(0, data=result)
