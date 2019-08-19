import json

from api.shortcuts import Response


def loop_deal_id(func):
    def wrapper(self, request, *args, **kargs):
        try:
            ids_list = json.loads(request.POST.get('id'))
        except TypeError:
            return Response(2)

        if isinstance(ids_list, list):
            result = []
            for i in ids_list:
                request.pk = i
                result.append(func(self, request, *args, **kargs))
            return Response(0, data=result, convert=True)

        if isinstance(ids_list, int):
            request.pk = ids_list
            return Response(0, data=func(self, request, *args, **kargs), convert=True)
        return Response(2, convert=True)

    return wrapper
