# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_auto_20160203_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardaccesslog',
            name='agent',
            field=models.TextField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='dashboardaccesslog',
            name='data',
            field=models.TextField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='dashboardaccesslog',
            name='url',
            field=models.TextField(default=None, null=True, blank=True),
        ),
    ]
