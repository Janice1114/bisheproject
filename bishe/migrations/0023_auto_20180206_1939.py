# Generated by Django 2.0 on 2018-02-06 11:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bishe', '0022_auto_20180202_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='count',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_count', models.IntegerField(default=0, verbose_name='用户数量')),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='card_number',
            field=models.CharField(default=0, max_length=50, verbose_name=''),
        ),
        migrations.AddField(
            model_name='store',
            name='store_registerName',
            field=models.CharField(default='', max_length=50, verbose_name='注册名字'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 6, 19, 39, 27, 474746), verbose_name='成交时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 6, 19, 39, 27, 470745), verbose_name='注册时间'),
        ),
    ]
