# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oppia', '0010_move_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='download_url',
            field=models.URLField(max_length=250),
        ),
    ]
