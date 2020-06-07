# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from settings import constants


def add_ipstack_apikey_setting(apps, schema_editor):

    props = apps.get_model("settings", "SettingProperties")
    try:
        props.objects.get(key=constants.OPPIA_IPSTACK_APIKEY)
    except props.DoesNotExist:
        settings_prop = props()
        settings_prop.key = constants.OPPIA_IPSTACK_APIKEY
        settings_prop.str_value = ''
        settings_prop.save()


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0012_map_config_setting'),
    ]

    operations = [
        migrations.RunPython(add_ipstack_apikey_setting),
    ]
