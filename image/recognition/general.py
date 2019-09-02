from api.exception import ClientError
from api.shortcuts import Response, request_check
from external.package import baidu


@request_check(
    url=(str, True),
)
def general_recognition(request):
    url = request.post.get('url')
    try:
        result = baidu.image_detect(url)['result']
    except KeyError:
        raise ClientError('图片格式错误')

    count = 0
    data = ''
    for i in result:
        data += f'猜测结果: {i["keyword"]}({i["root"]}), 确信度: {i["score"]:.2f}\n'
        count += 1
        if count >= 2:
            break
    return Response(request, 0, data=data)
