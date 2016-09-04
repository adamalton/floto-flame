# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('floto', '0002_auto_20160904_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='ignore',
            field=models.BooleanField(default=False, help_text=b"Ignore this album for display purposes? E.g. for the 'Auto upload' album."),
        ),
    ]
