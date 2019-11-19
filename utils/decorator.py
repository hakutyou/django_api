from rest_framework import decorators


def api_view(http_method_names):
    return decorators.api_view(http_method_names=http_method_names)
