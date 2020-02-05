# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
from settings.models import SettingProperties

from settings import constants


def add_map_viz_setting(apps, schema_editor):

    props = apps.get_model("settings", "SettingProperties")
    try:
        props.objects.get(key=constants.OPPIA_MAP_VISUALISATION_ENABLED)
    except props.DoesNotExist:
        settings_prop = props()
        settings_prop.key = constants.OPPIA_MAP_VISUALISATION_ENABLED
        settings_prop.bool_value = False
        settings_prop.save()


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0011_move_reg_to_bool'),
    ]

    operations = [
        migrations.RunPython(add_map_viz_setting),
    ]
