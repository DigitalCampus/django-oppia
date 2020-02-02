# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from settings.models import SettingProperties

from settings import constants


def insert_cartodb(apps, schema_editor):

    props = apps.get_model("settings", "SettingProperties")

    try:
        props.objects.get(key=constants.OPPIA_CARTODB_ACCOUNT)
    except props.DoesNotExist:
        settings_prop = props()
        settings_prop.key = constants.OPPIA_CARTODB_ACCOUNT
        settings_prop.str_value = None
        settings_prop.save()

    try:
        props.objects.get(key=constants.OPPIA_CARTODB_KEY)
    except props.DoesNotExist:
        settings_prop = props()
        settings_prop.key = constants.OPPIA_CARTODB_KEY
        settings_prop.str_value = None
        settings_prop.save()


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0005_insert_self_registration'),
    ]

    operations = [
        migrations.RunPython(insert_cartodb),
    ]
