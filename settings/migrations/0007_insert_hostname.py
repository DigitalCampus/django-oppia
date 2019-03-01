# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
from settings.models import SettingProperties

from settings import constants


def insert_hostname(apps, schema_editor):
    current = SettingProperties.get_string(constants.OPPIA_HOSTNAME, None)
    if current is None:
        SettingProperties.set_string(constants.OPPIA_HOSTNAME, None)

class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0006_insert_cartodb'),
    ]

    operations = [
        migrations.RunPython(insert_hostname),
    ]
