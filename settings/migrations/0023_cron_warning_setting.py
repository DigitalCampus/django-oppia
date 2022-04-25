# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
from django.utils.translation import ugettext_lazy as _

from settings import constants


def add_cron_warning_setting(apps, schema_editor):

    props = apps.get_model("settings", "SettingProperties")
    try:
        props.objects.get(key=constants.OPPIA_CRON_WARNING_HOURS)
    except props.DoesNotExist:
        settings_prop = props()
        settings_prop.key = constants.OPPIA_CRON_WARNING_HOURS
        settings_prop.description = _(
            u"Number of hours since last cron warning threshold")
        settings_prop.category = constants.SETTING_CATEGORY_SYSTEM_CONFIG
        settings_prop.int_value = 24 # default 1 day
        settings_prop.save()


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0022_edit_profile_setting'),
    ]

    operations = [
        migrations.RunPython(add_cron_warning_setting),
    ]
