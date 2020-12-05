# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.utils.translation import ugettext_lazy as _

from settings import constants


def add_badge_threshold_setting(apps, schema_editor):

    props = apps.get_model("settings", "SettingProperties")
    try:
        props.objects.get(key=constants.OPPIA_BADGES_PERCENT_COMPLETED)
    except props.DoesNotExist:
        settings_prop = props()
        settings_prop.key = constants.OPPIA_BADGES_PERCENT_COMPLETED
        settings_prop.int_value = 80
        settings_prop.description = _(u"If the badging is set to all quizzes \
            plus a percetntage of all other activities, what will that \
            percentage be")
        settings_prop.save()


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0016_setting_descriptions'),
    ]

    operations = [
        migrations.RunPython(add_badge_threshold_setting),
    ]