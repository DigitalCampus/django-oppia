# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from settings import constants


# Updates the settingproperties to give default category
def add_categories(apps, schema_editor):

    props = apps.get_model("settings", "SettingProperties")

    # System config
    add_setting_category(props,
                         constants.MAX_UPLOAD_SIZE,
                         constants.SETTING_CATEGORY_SYSTEM_CONFIG)
    add_setting_category(props,
                         constants.OPPIA_ALLOW_SELF_REGISTRATION,
                         constants.SETTING_CATEGORY_SYSTEM_CONFIG)
    add_setting_category(props,
                         constants.OPPIA_HOSTNAME,
                         constants.SETTING_CATEGORY_SYSTEM_CONFIG)
    add_setting_category(props,
                         constants.OPPIA_SHOW_GRAVATARS,
                         constants.SETTING_CATEGORY_SYSTEM_CONFIG)
    add_setting_category(props,
                         constants.OPPIA_DATA_RETENTION_YEARS,
                         constants.SETTING_CATEGORY_SYSTEM_CONFIG)

    # gamification
    add_setting_category(props,
                         constants.OPPIA_POINTS_ENABLED,
                         constants.SETTING_CATEGORY_GAMIFICATION)
    add_setting_category(props,
                         constants.OPPIA_BADGES_ENABLED,
                         constants.SETTING_CATEGORY_GAMIFICATION)
    add_setting_category(props,
                         constants.OPPIA_BADGES_PERCENT_COMPLETED,
                         constants.SETTING_CATEGORY_GAMIFICATION)

    # certification
    add_setting_category(props,
                         constants.OPPIA_EMAIL_CERTIFICATES,
                         constants.SETTING_CATEGORY_CERTIFICATION)

    # analytics
    add_setting_category(props,
                         constants.OPPIA_GOOGLE_ANALYTICS_ENABLED,
                         constants.SETTING_CATEGORY_ANALYTICS)
    add_setting_category(props,
                         constants.OPPIA_GOOGLE_ANALYTICS_CODE,
                         constants.SETTING_CATEGORY_ANALYTICS)
    add_setting_category(props,
                         constants.OPPIA_GOOGLE_ANALYTICS_DOMAIN,
                         constants.SETTING_CATEGORY_ANALYTICS)

    # app
    add_setting_category(props,
                         constants.OPPIA_ANDROID_ON_GOOGLE_PLAY,
                         constants.SETTING_CATEGORY_APP)
    add_setting_category(props,
                         constants.OPPIA_ANDROID_PACKAGEID,
                         constants.SETTING_CATEGORY_APP)

    # visualisations
    add_setting_category(props,
                         constants.OPPIA_MAP_VISUALISATION_ENABLED,
                         constants.SETTING_CATEGORY_VISUALISATIONS)
    add_setting_category(props,
                         constants.OPPIA_CARTODB_ACCOUNT,
                         constants.SETTING_CATEGORY_VISUALISATIONS)
    add_setting_category(props,
                         constants.OPPIA_CARTODB_KEY,
                         constants.SETTING_CATEGORY_VISUALISATIONS)
    add_setting_category(props,
                         constants.OPPIA_IPSTACK_APIKEY,
                         constants.SETTING_CATEGORY_VISUALISATIONS)

    # server registration
    add_setting_category(props,
                         constants.OPPIA_SERVER_REGISTERED,
                         constants.SETTING_CATEGORY_SERVER_REGISTRATION)
    add_setting_category(props,
                         constants.OPPIA_SERVER_REGISTER_APIKEY,
                         constants.SETTING_CATEGORY_SERVER_REGISTRATION)
    add_setting_category(props,
                         constants.OPPIA_SERVER_REGISTER_NO_COURSES,
                         constants.SETTING_CATEGORY_SERVER_REGISTRATION)
    add_setting_category(props,
                         constants.OPPIA_SERVER_REGISTER_NO_USERS,
                         constants.SETTING_CATEGORY_SERVER_REGISTRATION)
    add_setting_category(props,
                         constants.OPPIA_SERVER_REGISTER_EMAIL_NOTIF,
                         constants.SETTING_CATEGORY_SERVER_REGISTRATION)
    add_setting_category(props,
                         constants.OPPIA_SERVER_REGISTER_NOTIF_EMAIL_ADDRESS,
                         constants.SETTING_CATEGORY_SERVER_REGISTRATION)
    add_setting_category(props,
                         constants.OPPIA_SERVER_REGISTER_LAST_SENT,
                         constants.SETTING_CATEGORY_SERVER_REGISTRATION)


def add_setting_category(props, key, category):
    try:
        prop = props.objects.get(key=key)
        prop.category = category
        prop.save()
    except props.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0019_settingproperties_category'),
    ]

    operations = [
        migrations.RunPython(add_categories),
    ]
