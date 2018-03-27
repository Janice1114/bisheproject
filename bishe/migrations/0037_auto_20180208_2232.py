# Generated by Django 2.0 on 2018-02-08 14:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bishe', '0036_auto_20180208_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 8, 22, 32, 26, 248611), verbose_name='成交时间'),
        ),
        migrations.AlterField(
            model_name='store',
            name='store_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 8, 22, 32, 26, 248611), editable=False, verbose_name='商店注册时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_img',
            field=models.ImageField(default='/userImage/default.png', upload_to='userImage'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 8, 22, 32, 26, 248611), editable=False, verbose_name='注册时间'),
        ),
    ]
