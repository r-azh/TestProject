# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-10 13:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0002_auto_20170910_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 10, 13, 47, 5, 948322, tzinfo=utc), verbose_name='Created Date'),
        ),
    ]