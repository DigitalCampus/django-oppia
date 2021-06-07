# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.utils.translation import ugettext_lazy as _

from settings import constants


def add_email_certs_setting(apps, schema_editor):

    props = apps.get_model("settings", "SettingProperties")
    try:
        props.objects.get(key=constants.OPPIA_EMAIL_CERTIFICATES)
    except props.DoesNotExist:
        settings_prop = props()
        settings_prop.key = constants.OPPIA_EMAIL_CERTIFICATES
        settings_prop.description = _(u"Whether or not certificates should be \
            emailed to users")
        settings_prop.bool_value = False
        settings_prop.save()


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0017_badge_threshold'),
    ]

    operations = [
        migrations.RunPython(add_email_certs_setting),
    ]
