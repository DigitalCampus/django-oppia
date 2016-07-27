# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0003_userpointssummary'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpointssummary',
            name='badges',
            field=models.IntegerField(default=0),
        ),
    ]
