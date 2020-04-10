import requests
from django.views.decorators.csrf import csrf_exempt

from api.shortcuts import Response, request_check
from external.service import scf_service


def scf_common(request, path):
    """
    转 SCF 调用，仅 demo 测试
    """
    data = request.POST.dict()
    result = scf_service.post(path, data=data)
    return Response(request, 0, msg=result)


@csrf_exempt
@request_check(
    url=(str, True),
    json=(str, False),
    method=(str, False)
)
def proxy_common(request):
    """
    转外网调用，私有网络（SCF）访问外网时使用
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/55.0.2883.87 Safari/537.36'
    }
    url = request.post.get('url')
    json = request.post.get('json')
    method = request.post.get('method')
    if method == 'get':
        response = requests.get(url, json=json, headers=headers)
    else:
        response = requests.post(url, json=json, headers=headers)
    return Response(request, 0, _type='str', data=response.text)
