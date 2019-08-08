from api.shortcuts import Response


def API_METHOD(method):
    def _api_method(func):
        def wrapper(request, *args, **kwargs):
            if request.method != method:
                return Response(4)
            return func(request, *args, **kwargs)

        return wrapper

    return _api_method
