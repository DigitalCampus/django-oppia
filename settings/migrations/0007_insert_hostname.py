# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from settings import constants


def insert_hostname(apps, schema_editor):

    props = apps.get_model("settings", "SettingProperties")

    try:
        props.objects.get(key=constants.OPPIA_HOSTNAME)
    except props.DoesNotExist:
        settings_prop = props()
        settings_prop.key = constants.OPPIA_HOSTNAME
        settings_prop.str_value = None
        settings_prop.save()


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0006_insert_cartodb'),
    ]

    operations = [
        migrations.RunPython(insert_hostname),
    ]
