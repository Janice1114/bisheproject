# Generated by Django 2.0 on 2018-02-09 08:13

import bishe.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bishe', '0044_auto_20180209_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 9, 16, 13, 32, 52331), verbose_name='成交时间'),
        ),
        migrations.AlterField(
            model_name='store',
            name='store_cover',
            field=models.ImageField(default='storeImage/default.png', upload_to=bishe.models.get_path, verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='store',
            name='store_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 9, 16, 13, 32, 52331), editable=False, verbose_name='商店注册时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 9, 16, 13, 32, 36708), editable=False, verbose_name='注册时间'),
        ),
    ]
