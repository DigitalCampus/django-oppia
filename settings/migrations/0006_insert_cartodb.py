# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from settings.models import SettingProperties

from settings import constants


def insert_cartodb(apps, schema_editor):
    current = SettingProperties.get_string(constants.OPPIA_CARTODB_ACCOUNT,
                                           None)
    if current is None:
        SettingProperties.set_string(constants.OPPIA_CARTODB_ACCOUNT, None)

    current = SettingProperties.get_string(constants.OPPIA_CARTODB_KEY, None)
    if current is None:
        SettingProperties.set_string(constants.OPPIA_CARTODB_KEY, None)


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0005_insert_self_registration'),
    ]

    operations = [
        migrations.RunPython(insert_cartodb),
    ]
