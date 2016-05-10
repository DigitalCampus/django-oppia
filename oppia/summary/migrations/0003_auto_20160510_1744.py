# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0002_auto_20160510_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercoursesummary',
            name='pretest_score',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
