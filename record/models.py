from django.db import models


# Create your models here.
class RecordItem(models.Model):
    create_date = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'record_item'
        verbose_name = '记录'
        verbose_name_plural = verbose_name
