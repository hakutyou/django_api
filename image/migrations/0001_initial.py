# Generated by Django 2.2.7 on 2019-11-19 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FaceUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=32, verbose_name='用户ID')),
                ('user_name', models.CharField(max_length=32, verbose_name='用户名')),
                ('face_image', models.CharField(max_length=256, verbose_name='用户人脸图片')),
                ('face_token', models.CharField(max_length=32, verbose_name='百度人脸 token')),
                ('group_id', models.CharField(max_length=32, verbose_name='组ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '人脸用户',
                'verbose_name_plural': '人脸用户',
                'db_table': 'face_user',
                'unique_together': {('user_id', 'group_id')},
            },
        ),
    ]