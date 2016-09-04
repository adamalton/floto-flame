# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import floto.fields


class Migration(migrations.Migration):

    dependencies = [
        ('floto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='photo',
            name='date_taken',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='location',
            field=floto.fields.JSONField(default=dict, blank=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='albums',
            field=models.ManyToManyField(to='floto.Album'),
        ),
    ]
