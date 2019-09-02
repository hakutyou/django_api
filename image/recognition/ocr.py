from api.shortcuts import Response, request_check
from external.package import baidu


@request_check(
    url=(str, True),
    lang=(str, True),
)
def general_ocr(request):
    url = request.post.get('url')
    lang = request.post.get('lang')
    try:
        result = baidu.ocr_basic(url, lang)['words_result']
    except KeyError:
        return Response(0, data='图片格式错误')

    data = ''
    for i in result:
        data += f'{i["words"]}\n'
    return Response(request, 0, data=data)
