from rest_framework import generics
from rest_framework.mixins import ListModelMixin
from rest_framework.settings import api_settings

from .models import RecordItem
from .serializer import RecordItemSerializer


# Create your views here.
class RecordItemView(ListModelMixin,
                     generics.GenericAPIView):
    queryset = RecordItem.objects.all()
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    serializer_class = RecordItemSerializer
    filter_check = ['name', 'sex', 'occupation']

    def filter_queryset(self, queryset):
        extra = {}
        for i in self.filter_check:
            field = self.request.query_params.get(i)
            if field:
                extra.update({i: field})
        return queryset.filter(**extra)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


record_item_view = RecordItemView.as_view()
