from django.db import models


# Create your models here.
class CoolqReply(models.Model):
    pattern = models.CharField('输入内容', max_length=256, db_index=True)
    reply = models.CharField('输出内容', max_length=256)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    create_qq = models.CharField('创建者', max_length=15)
    group_id = models.IntegerField('回复QQ群')
    status = models.BooleanField('是否开启', default=True)
    # 默认延迟 200 毫秒后回复
    delay = models.IntegerField('延迟回复', default=200)

    from_title = models.ForeignKey(
        'qchat.CoolqSubject', verbose_name='需要话题', related_name='to_reply',
        on_delete=models.CASCADE, null=True)
    to_title = models.ForeignKey(
        'qchat.CoolqSubject', verbose_name='进入话题', related_name='from_reply',
        on_delete=models.CASCADE)

    class Meta:
        db_table = 'coolq_reply'
        verbose_name = '回复库'
        verbose_name_plural = verbose_name


class CoolqSubject(models.Model):
    subject = models.CharField('主题名称', max_length=64, db_index=True)

    class Meta:
        db_table = 'coolq_subject'
        verbose_name = '回复状态库'
        verbose_name_plural = verbose_name
