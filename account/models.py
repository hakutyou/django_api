from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class UserModels(AbstractUser):
    mobile = models.CharField('手机号', max_length=20, unique=True,
                              error_messages={
                                  'unique': "该手机号已使用",
                              })

    class Meta:
        db_table = 'account'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
