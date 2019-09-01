import json

from rest_framework import decorators

from api.exception import ServiceError
from api.shortcuts import Response


def loop_deal_id(func):
    def wrapper(self, request, *args, **kargs):
        try:
            ids_list = json.loads(request.POST.get('id'))
        except TypeError:
            raise ServiceError('Argument Error', code=400)

        if isinstance(ids_list, list):
            result = []
            for i in ids_list:
                request.pk = i
                result.append(func(self, request, *args, **kargs))
            return Response(request, 0, data=result)

        if isinstance(ids_list, int):
            request.pk = ids_list
            return func(self, request, *args, **kargs)
        raise ServiceError('Argument Error', code=400)

    return wrapper


def api_view(http_method_names):
    return decorators.api_view(http_method_names=http_method_names)
