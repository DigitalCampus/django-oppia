# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
from settings.models import SettingProperties

from settings import constants


def insert_maxuploadsize(apps, schema_editor):
    props = apps.get_model("settings", "SettingProperties")

    try:
        props.objects.get(key=constants.MAX_UPLOAD_SIZE)
    except props.DoesNotExist:
        if hasattr(settings, 'OPPIA_MAX_UPLOAD_SIZE'):
            settings_prop = props()
            settings_prop.key = constants.MAX_UPLOAD_SIZE
            settings_prop.int_value = settings.OPPIA_MAX_UPLOAD_SIZE
            settings_prop.save()


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_auto_20170628_1923'),
    ]

    operations = [
        migrations.RunPython(insert_maxuploadsize),
    ]
