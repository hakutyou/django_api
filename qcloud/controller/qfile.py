from django.shortcuts import HttpResponse
from qcloud_cos import CosClientError, CosServiceError

# from account.controller.account import require_permission
from api.shortcuts import Response
from external.interface import tencent_cos_service


# @require_permission(1 << 0)
def get_file_list(_, path):
    response = tencent_cos_service.list(path=path[1:])
    files = []
    directories = []

    for file in response.get('Contents', []):
        filename = file['Key']
        if filename[-1] == '/':
            continue
        files.append(filename)

    for directory in response.get('CommonPrefixes', []):
        directories.append(directory['Prefix'])

    data = {'file': files,
            'directory': directories}
    return Response(0, data=data)


# @require_permission(1 << 1)
def get_file_info(request, path):
    try:
        response = tencent_cos_service.file(path=path)
    except CosClientError as e:
        return Response(-1, str(e), 'CosClientError')
    except CosServiceError as e:
        return Response(-1, str(e), 'CosServiceError')

    _type = response['Content-Type']
    if request.POST.get('detail', None) is None:
        data = {'type': _type, 'length': response['Content-Length']}
        return Response(0, data=data)
    else:
        with response['Body'].get_raw_stream() as fp:
            content = fp.read()
            return HttpResponse(content, content_type=_type)
