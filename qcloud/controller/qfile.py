from django.shortcuts import HttpResponse
from qcloud_cos import CosClientError, CosServiceError

# from account.controller.auth import require_permission
from api.shortcuts import Response
from qcloud.config import *


# @require_permission(1 << 0)
def get_file_list(_, offset):
    response = client.list_objects(Bucket=bucket, Prefix=offset,
                                   Delimiter='/', MaxKeys=10)
    data = {'file': response.get('Contents', []),
            'directory': response.get('CommonPrefixes', [])}
    return Response(0, data=data)


# @require_permission(1 << 1)
def get_file_info(request, offset):
    try:
        response = client.get_object(Bucket=bucket, Key=offset)
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
