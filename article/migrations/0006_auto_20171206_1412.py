# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-06 06:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_auto_20171205_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 6, 6, 12, 18, 722524, tzinfo=utc)),
        ),
    ]
