# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0003_insert_initial_uploadsize'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='settingproperties',
            options={'ordering': ['key'], 'verbose_name': 'Settings', 'verbose_name_plural': 'Settings'},
        ),
    ]
