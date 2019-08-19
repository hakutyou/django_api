import django_filters
from django.db import models


# Create your models here.
class RecordItem(models.Model):
    create_date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=128)
    sex = models.IntegerField()
    occupation = models.IntegerField()

    class Meta:
        db_table = 'record_item'
        verbose_name = '记录'
        verbose_name_plural = verbose_name


class RecordItemFilter(django_filters.FilterSet):
    # sort = django_filters.OrderingFilter(fields=('create_date',))
    SEX_CHOICE = (
        (0, 'female'),
        (1, 'male'),
    )
    name = django_filters.CharFilter('name', lookup_expr='icontains')
    sex = django_filters.ChoiceFilter('sex', choices=SEX_CHOICE)
    start_date = django_filters.DateFilter('create_date', lookup_expr='gte')
    end_date = django_filters.DateFilter('create_date', lookup_expr='lte')

    class Meta:
        model = RecordItem
        fields = ['name', 'sex', 'start_date', 'end_date']