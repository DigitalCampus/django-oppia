# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0003_userpointssummary'),
    ]

    database_operations = [
        migrations.AlterModelTable(
            name='SettingProperties',
            table='settings_settingproperties'
        )
    ]

    state_operations = [
        migrations.DeleteModel(name='SettingProperties'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations)
    ]
