# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-08 09:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_auto_20171206_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 8, 9, 51, 45, 532114, tzinfo=utc)),
        ),
    ]