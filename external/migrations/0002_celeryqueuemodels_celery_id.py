# Generated by Django 2.2.7 on 2020-04-09 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('external', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='celeryqueuemodels',
            name='celery_id',
            field=models.CharField(default='', max_length=64, verbose_name='celery 的标识码'),
        ),
    ]