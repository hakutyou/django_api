import django_filters
from django.db import models


# Create your models here.
class DictKanaItem(models.Model):
    kana = models.CharField('かな', unique=True, max_length=64)
    # kanji = One To Many DictKanjiItem
    # create_time = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    update_date = models.DateField('更新时间', auto_now=True)

    class Meta:
        db_table = 'dict_kana_table'
        ordering = ['id']
        verbose_name = 'かな表'
        verbose_name_plural = verbose_name


class DictKanjiItem(models.Model):
    HINSI_CHOICE = (
        ('meisi', '名詞'),
        ('dousi', '動詞'),
    )
    kana = models.ForeignKey('record.DictKanaItem', related_name='kanji', on_delete=models.PROTECT)
    kanji = models.CharField('漢字', unique=True, max_length=64, default='')
    imi = models.CharField('意味', max_length=256, default='')

    # dougi = Many To Many DictDougi
    # score = One To Many DictScore
    theta = models.FloatField('シータ', default=1.0)
    hinnsi = models.CharField('品词', max_length=64, choices=HINSI_CHOICE)
    rei = models.TextField('例')
    # create_time = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    update_date = models.DateField('更新时间', auto_now=True)

    class Meta:
        db_table = 'dict_kanji_table'
        verbose_name = '漢字表'
        verbose_name_plural = verbose_name

    @classmethod
    def get_verbose_name(cls, field, name, default=None):
        """
        返回相当于 get__display 的数据
        DictKanjiItem.get_verbose_name('hinnsi', 'meisi')
        => '名詞', 相当于 get_HINSI_CHOICE_display()
        """
        field = cls._meta.get_field(field)
        return dict(field.flatchoices).get(name, default)


class DictDougi(models.Model):
    imi = models.ManyToManyField('record.DictKanjiItem', related_name='dougi')
    dougi = models.CharField('説明', max_length=256, default='')
    rei = models.TextField('例', default='')
    # create_time = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    update_date = models.DateField('更新时间', auto_now=True)

    class Meta:
        db_table = 'dict_dougi_table'
        verbose_name = '同義語表'
        verbose_name_plural = verbose_name


class DictScore(models.Model):
    next_date = models.DateField('次回の時間')
    score = models.CharField('アカウント点数', max_length=128, default='')
    account = models.ForeignKey('account.UserModels', on_delete=models.CASCADE)
    kanji = models.ForeignKey('record.DictKanjiItem', related_name='score', on_delete=models.CASCADE)
    # create_time = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    update_date = models.DateField('更新时间', auto_now=True)

    class Meta:
        unique_together = ('account', 'kanji',)
        db_table = 'dict_score_table'
        verbose_name = 'アカウント点数表'
        verbose_name_plural = verbose_name


# Filter 部分
class DictKanaItemFilter(django_filters.FilterSet):
    kana = django_filters.CharFilter('kana', lookup_expr='icontains')

    class Meta:
        models = DictKanaItem
        fields = ['kana']


class DictKanjiItemFilter(django_filters.FilterSet):
    kanji = django_filters.CharFilter('kanji', lookup_expr='icontains')

    class Meta:
        models = DictKanjiItem
        fields = ['kanji']
