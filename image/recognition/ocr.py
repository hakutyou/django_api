from api.shortcuts import Response
from external.package import baidu


def general_ocr(request):
    try:
        url = request.POST['url']
        lang = request.POST['lang']
    except KeyError:
        return Response(2)

    try:
        result = baidu.ocr_basic(url, lang)['words_result']
    except KeyError:
        return Response(0, data='图片格式错误')

    data = ''
    for i in result:
        data += f'{i["words"]}\n'
    return Response(0, data=data)
