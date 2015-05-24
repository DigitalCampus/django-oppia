# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlocationvisualization',
            name='ip',
            field=models.GenericIPAddressField(),
            preserve_default=True,
        ),
    ]
