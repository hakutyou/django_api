from django.views.decorators.csrf import csrf_exempt

from api.exception import ClientError
from api.shortcuts import Response, request_check
from external.interface import ocr_service


@csrf_exempt
@request_check(
    url=(str, True),
    lang=(str, True),
)
def general_ocr(request):
    url = request.post.get('url')
    lang = request.post.get('lang')
    try:
        result = ocr_service.ocr_general(url, lang)
    except KeyError:
        raise ClientError('图片格式错误', code=401)
        # return Response(request, 0, data='图片格式错误')

    data = ''
    # for i in result:
    #     data += f'{i["words"]}\n'
    return Response(request, 0, data=result)
