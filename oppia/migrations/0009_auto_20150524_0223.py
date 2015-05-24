# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oppia', '0008_auto_20150524_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracker',
            name='ip',
            field=models.GenericIPAddressField(),
            preserve_default=True,
        ),
    ]
