# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-18 19:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('floto', '0004_auto_20160904_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='date_taken_granularity',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
