from django.http import JsonResponse
from rest_framework import pagination


class DefaultPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return JsonResponse({
            'page': self.page.number,
            'page_count': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'results': data
        })


class SerialPagination(pagination.PageNumberPagination):
    """
    用于不能跳页的方法
    """

    def get_paginated_response(self, data):
        return JsonResponse({
            'page': self.page.number,
            'have_next': self.page.has_next(),
            'have_prev': self.page.has_previous(),
            'results': data,
        })
