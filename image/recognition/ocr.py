from api.shortcuts import Response, request_check
from external.interface import tencent_ocr_service, baidu_ocr_service


@request_check(
    url=(str, True),
    lang=(str, True),
)
def general_ocr(request):
    url = request.post.get('url')
    lang = request.post.get('lang')
    try:
        result = baidu_ocr_service.ocr_basic(url, lang)['words_result']
    except KeyError:
        return Response(0, data='图片格式错误')

    data = ''
    for i in result:
        data += f'{i["words"]}\n'
    return Response(request, 0, data=data)


@request_check(
    url=(str, True),
)
def tencent_general_ocr(request):
    url = request.post.get('url')
    response = tencent_ocr_service.ocr_general(url)
    if response['msg'] != 'ok':
        return Response(request, 1, _type='str', data=response['msg'])
    data = []
    for i in response['data']['item_list']:
        data.append(i['itemstring'])
    return Response(request, 0, data=data)
