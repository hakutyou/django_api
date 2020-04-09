from django.db import models


# Create your models here.
class CeleryQueueModels(models.Model):
    STATUS = (
        (0, '加入队列'),
        (1, '进行中'),
        (2, '成功'),
        (3, '失败'),
    )
    ic = models.CharField('标识码', max_length=20)
    # yyyy mmdd HHMM SSrr rrrr
    _type = models.CharField('类型', max_length=8)
    celery_id = models.CharField('celery 的标识码', max_length=64, default='')
    status = models.IntegerField(default=0)

    class Meta:
        unique_together = ('ic', '_type')
        db_table = 'celery_queue'
        verbose_name = 'Celery 任务队列'
        verbose_name_plural = verbose_name
