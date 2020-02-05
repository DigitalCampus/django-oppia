# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
from settings.models import SettingProperties

from settings import constants


def move_reg_to_bool_setting(apps, schema_editor):

    props = apps.get_model("settings", "SettingProperties")
    try:
        current_prop = props.objects.get(
            key=constants.OPPIA_ALLOW_SELF_REGISTRATION)
        if current_prop.int_value == 0:
            current_prop.bool_value = False
        else:
            current_prop.bool_value = True
        current_prop.int_value = None
        current_prop.save()
    except props.DoesNotExist:
        settings_prop = props()
        settings_prop.key = constants.OPPIA_ALLOW_SELF_REGISTRATION
        if hasattr(settings, 'OPPIA_ALLOW_SELF_REGISTRATION'):
            settings_prop.bool_value = settings.OPPIA_ALLOW_SELF_REGISTRATION
        else:
            settings_prop.bool_value = True
        settings_prop.save()


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0010_move_to_settings'),
    ]

    operations = [
        migrations.RunPython(move_reg_to_bool_setting),
    ]
