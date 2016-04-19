# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardaccesslog',
            name='ip',
            field=models.GenericIPAddressField(default=None, null=True, blank=True),
        ),
    ]
