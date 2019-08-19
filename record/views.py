from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.mixins import ListModelMixin, DestroyModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.settings import api_settings

from api.shortcuts import Response
from .models import RecordItem, RecordItemFilter
from .serializer import RecordItemSerializer


# Create your views here.
class RecordItemView(ListModelMixin,
                     UpdateModelMixin,
                     DestroyModelMixin,
                     CreateModelMixin,
                     generics.GenericAPIView):
    queryset = RecordItem.objects.all()
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    serializer_class = RecordItemSerializer
    filterset_class = RecordItemFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    def get_object(self):
        return self.queryset.get(id=self.request.pk)

    # 查询
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # 删除
    def delete(self, request, *args, **kwargs):
        request.pk = request.POST.get('id')
        try:
            return self.destroy(request, *args, **kwargs)  # 204 表示删除成功
        except RecordItem.DoesNotExist:
            return Response(270, convert=True)

    # 增加
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # 修改
    def put(self, request, *args, **kwargs):
        request.pk = request.POST.get('id')
        return self.partial_update(request, *args, **kwargs)


record_item_view = RecordItemView.as_view()
