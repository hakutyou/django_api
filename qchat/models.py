from django.db import models


# Create your models here.
class CoolqReply(models.Model):
    pattern = models.CharField('输入内容', max_length=256, db_index=True)
    reply = models.CharField('输出内容', max_length=256)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    create_qq = models.CharField('创建者', max_length=15)
    group_id = models.IntegerField('回复QQ群')
    status = models.BooleanField('是否开启', default=True)
    regex = models.BooleanField('正则', default=False)

    from_title = models.CharField('需要话题', max_length=128, default=None, null=True, db_index=True)
    to_title = models.CharField('进入话题', max_length=128, default=None, null=True)

    class Meta:
        db_table = 'coolq_reply'
        verbose_name = '回复库'
        verbose_name_plural = verbose_name
