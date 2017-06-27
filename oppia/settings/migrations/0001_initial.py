# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0004_delete_settingproperties'),
    ]

    state_operations = [
        migrations.CreateModel(
            name='SettingProperties',
            fields=[
                ('key', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('str_value', models.CharField(max_length=50, null=True, blank=True)),
                ('int_value', models.IntegerField()),
            ],
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]
