# Generated by Django 2.0 on 2018-03-17 05:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bishe', '0075_auto_20180314_2313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='store_card_style',
        ),
        migrations.AddField(
            model_name='store',
            name='store_card_discount',
            field=models.TextField(default=0, verbose_name='会员折扣划分'),
        ),
        migrations.AddField(
            model_name='store',
            name='store_card_prefix',
            field=models.CharField(default=0, max_length=50, verbose_name='会员卡前缀'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 17, 13, 12, 53, 142486), verbose_name='成交时间'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='stock_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 17, 13, 12, 53, 142486), verbose_name='入库日期'),
        ),
        migrations.AlterField(
            model_name='store',
            name='store_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 17, 13, 12, 53, 126857), editable=False, verbose_name='商店注册时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 17, 13, 12, 53, 126857), editable=False, verbose_name='注册时间'),
        ),
    ]
