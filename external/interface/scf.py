import requests

from api.shortcuts import Response, request_check
from external.service import scf_service


def scf_common(request, path):
    """
    转 SCF 调用，仅 demo 测试
    """
    data = request.POST.dict()
    result = scf_service.post(path, data=data)
    return Response(request, 0, msg=result)


@request_check(
    url=(str, True),
    json=(str, False)
)
def proxy_common(request):
    """
    转外网调用，私有网络（SCF）访问外网时使用
    """
    url = request.post.get('url')
    json = request.post.get('json')
    response = requests.post(url, json=json)
    return Response(request, 0, _type='str', data=response.text)
