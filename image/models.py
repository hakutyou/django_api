from django.db import models


class FaceUser(models.Model):
    user_id = models.CharField('用户ID', max_length=32)
    user_name = models.CharField('用户名', max_length=32)
    face_image = models.CharField('用户人脸图片', max_length=256)
    face_token = models.CharField('百度人脸 token', max_length=32)
    group_id = models.CharField('组ID', max_length=32)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        unique_together = ('user_id', 'group_id')
        db_table = 'face_user'
        verbose_name = '人脸用户'
        verbose_name_plural = verbose_name
