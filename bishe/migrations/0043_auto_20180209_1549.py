# Generated by Django 2.0 on 2018-02-09 07:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bishe', '0042_auto_20180209_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 9, 15, 49, 4, 832213), verbose_name='成交时间'),
        ),
        migrations.AlterField(
            model_name='store',
            name='store_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 9, 15, 49, 4, 816573), editable=False, verbose_name='商店注册时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 9, 15, 49, 4, 816573), editable=False, verbose_name='注册时间'),
        ),
    ]
