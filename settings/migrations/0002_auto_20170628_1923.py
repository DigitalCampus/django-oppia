# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='settingproperties',
            options={'ordering': ['key'], 'verbose_name': 'Settings'},
        ),
        migrations.AlterField(
            model_name='settingproperties',
            name='int_value',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
