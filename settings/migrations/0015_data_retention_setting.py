# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from settings import constants


def add_data_retention_setting(apps, schema_editor):

    props = apps.get_model("settings", "SettingProperties")
    try:
        props.objects.get(key=constants.OPPIA_DATA_RETENTION_YEARS)
    except props.DoesNotExist:
        settings_prop = props()
        settings_prop.key = constants.OPPIA_DATA_RETENTION_YEARS
        settings_prop.int_value = 7
        settings_prop.save()


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0014_settingproperties_description'),
    ]

    operations = [
        migrations.RunPython(add_data_retention_setting),
    ]
