from api.shortcuts import Response
from external.package import baidu


def general_recognition(request):
    try:
        url = request.POST['url']
    except KeyError:
        return Response(2)

    try:
        result = baidu.image_detect(url)['result']
    except KeyError:
        return Response(0, data='图片格式错误')

    count = 0
    data = ''
    for i in result:
        data += f'猜测结果: {i["keyword"]}({i["root"]}), 确信度: {i["score"]:.2f}\n'
        count += 1
        if count >= 2:
            break
    return Response(0, data=data)
