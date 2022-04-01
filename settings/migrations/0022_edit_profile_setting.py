# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
from django.utils.translation import gettext_lazy as _

from settings import constants


def add_profile_editing_setting(apps, schema_editor):

    props = apps.get_model("settings", "SettingProperties")
    try:
        props.objects.get(key=constants.OPPIA_ALLOW_PROFILE_EDITING)
    except props.DoesNotExist:
        settings_prop = props()
        settings_prop.key = constants.OPPIA_ALLOW_PROFILE_EDITING
        settings_prop.description = _(
            u"Allow normal users to edit their profiles")
        settings_prop.category = constants.SETTING_CATEGORY_SYSTEM_CONFIG
        settings_prop.bool_value = settings.OPPIA_ALLOW_PROFILE_EDITING
        settings_prop.save()


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0021_auto_20210816_1057'),
    ]

    operations = [
        migrations.RunPython(add_profile_editing_setting),
    ]
