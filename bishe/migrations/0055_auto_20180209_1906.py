# Generated by Django 2.0 on 2018-02-09 11:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bishe', '0054_auto_20180209_1644'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='store_cov',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 9, 19, 6, 41, 642954), verbose_name='成交时间'),
        ),
        migrations.AlterField(
            model_name='store',
            name='store_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 9, 19, 6, 41, 642954), editable=False, verbose_name='商店注册时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 9, 19, 6, 41, 642954), editable=False, verbose_name='注册时间'),
        ),
    ]
