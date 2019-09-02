from qcloud_cos import CosClientError, CosServiceError

# from account.controller.account import require_permission
from api.exception import ServiceError
from api.shortcuts import Response, request_check
from external.interface import tencent_cos_service


# @require_permission(1 << 0)
def get_file_list(request, path):
    response = tencent_cos_service.list(path=path)
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
    return Response(request, 0, data=data)


# @require_permission(1 << 1)
@request_check(
    detail=(str, False)
)
def get_file_info(request, path):
    try:
        response = tencent_cos_service.file(path=path)
    except CosClientError as e:
        raise ServiceError(str(e), code=-1)
    except CosServiceError as e:
        raise ServiceError(e.get_error_msg(), code=-2)

    content_type = response['Content-Type']
    if request.post.get('detail') is None:
        data = {'type': content_type, 'length': response['Content-Length']}
        return Response(request, 0, data=data)
    else:
        with response['Body'].get_raw_stream() as fp:
            content = fp.read()
            return Response(request, 0, _type='str', data=content, content_type=content_type)


@request_check(
    path=(str, True),
    bucket=(str, False)
)
def upload_file(request):
    path = request.post.get('path')
    bucket = request.post.get('bucket')
    try:
        content = tencent_cos_service.upload(request.byte_stream, path=path, bucket=bucket)
    except CosClientError as e:
        raise ServiceError(str(e), code=-1)
    except CosServiceError as e:
        raise ServiceError(e.get_error_msg(), code=-2)

    return Response(request, 0, _type='str', data=content)
