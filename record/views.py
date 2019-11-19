from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.mixins import ListModelMixin, DestroyModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.settings import api_settings

from api.exception import ServiceError
from api.shortcuts import Response
from .models import DictKanaItem, DictKanaItemFilter, DictKanjiItem, DictKanjiItemFilter
from .serializer import DictKanaItemSerializer, DictKanjiItemSerializer


# Create your views here.
# かな検測
class DictKanaItemView(ListModelMixin,
                       UpdateModelMixin,
                       DestroyModelMixin,
                       CreateModelMixin,
                       generics.GenericAPIView):
    queryset = DictKanaItem.objects.all()
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    serializer_class = DictKanaItemSerializer
    filter_class = DictKanaItemFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    def get_object(self):
        return self.queryset.get(id=self.request.pk)

    # 查询
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # 删除
    def delete(self, request, *args, **kwargs):
        # return self.destroy(request, *args, **kwargs)
        pks = request.POST.get('id').split(',')
        number, deleted_list = self.queryset.filter(id__in=pks).delete()
        return Response(request, 204, data=number)

    # 增加
    def post(self, request, *args, **kwargs):
        data = request.data.dict()
        kana = data.get('kana')
        kanji = data.get('kanji')
        if not kana or not kanji:
            raise ServiceError('Argument Error', code=400)
        # kana_query
        try:
            kana_query = self.queryset.get(kana=kana)
        except DictKanaItem.DoesNotExist:
            kana_query = self.queryset.create(kana=kana)
        # kanji_query
        try:
            kanji_query = kana_query.kanji.get(kanji=kanji)
        except DictKanjiItem.DoesNotExist:
            kanji_query = kana_query.kanji.create(
                kanji=data.get('kanji'),
            )
        kanji_query.theta = data.get('theta', 1.0)
        kanji_query.hinnsi = data.get('hinnsi', '')
        kanji_query.rei = data.get('rei', '')
        kanji_query.save(update_fields=['theta', 'hinnsi', 'rei'])
        return Response(request, 0)


# 漢字検測
class DictKanjiItemView(ListModelMixin,
                        DestroyModelMixin,
                        generics.GenericAPIView):
    queryset = DictKanjiItem.objects.all()
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    serializer_class = DictKanjiItemSerializer
    filter_class = DictKanjiItemFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    # 查询
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # 删除
    def delete(self, request, *args, **kwargs):
        # return self.destroy(request, *args, **kwargs)
        pks = request.POST.get('id').split(',')
        number, deleted_list = self.queryset.filter(id__in=pks).delete()
        return Response(request, 204, data=number)


dict_kana_item_view = DictKanaItemView.as_view()
dict_kanji_item_view = DictKanjiItemView.as_view()
