# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
from settings.models import SettingProperties

from settings import constants


def insert_self_registration(apps, schema_editor):
    props = apps.get_model("settings", "SettingProperties")

    try:
        props.objects.get(key=constants.OPPIA_ALLOW_SELF_REGISTRATION)
    except props.DoesNotExist:
        if hasattr(settings, 'OPPIA_ALLOW_SELF_REGISTRATION'):
            settings_prop = props()
            settings_prop.key = constants.OPPIA_ALLOW_SELF_REGISTRATION
            settings_prop.int_value = settings.OPPIA_ALLOW_SELF_REGISTRATION
            settings_prop.save()


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0004_auto_20171128_1715'),
    ]

    operations = [
        migrations.RunPython(insert_self_registration),
    ]
