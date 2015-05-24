# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oppia', '0007_auto_20150524_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='shortname',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
