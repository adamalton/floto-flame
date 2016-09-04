# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255, blank=True)),
                ('timestamp', models.DateTimeField(null=True, blank=True)),
                ('rotation', models.PositiveIntegerField(default=0)),
                ('url', models.URLField()),
                ('cached_image', models.FileField(null=True, upload_to=b'/Users/adamalton/Sites/github/floto-flame/.cache/images')),
            ],
        ),
    ]
