# Generated by Django 2.2.7 on 2019-11-20 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0003_auto_20191119_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='dictscore',
            name='update_date',
            field=models.DateField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='dictdougi',
            name='update_date',
            field=models.DateField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='dictkanaitem',
            name='update_date',
            field=models.DateField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AlterField(
            model_name='dictkanjiitem',
            name='update_date',
            field=models.DateField(auto_now=True, verbose_name='更新时间'),
        ),
    ]
