# Generated by Django 2.0 on 2018-02-01 12:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bishe', '0013_order_order_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 1, 20, 6, 48, 837830), verbose_name='成交时间'),
        ),
    ]
