# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations

from settings import constants


def move_to_settings(apps, schema_editor):

    props = apps.get_model("settings", "SettingProperties")
    move_gravatars(props)
    move_points(props)
    move_badges(props)
    move_ga(props)
    move_google_play(props)
    move_ga_code(props)
    move_ga_domain(props)
    move_packageid(props)


def move_gravatars(props):
    try:
        props.objects.get(key=constants.OPPIA_SHOW_GRAVATARS)
    except props.DoesNotExist:
        settings_prop = props()
        settings_prop.key = constants.OPPIA_SHOW_GRAVATARS
        if hasattr(settings, 'OPPIA_SHOW_GRAVATARS'):
            settings_prop.bool_value = settings.OPPIA_SHOW_GRAVATARS
        else:
            settings_prop.bool_value = True
        settings_prop.save()


def move_points(props):
    try:
        props.objects.get(key=constants.OPPIA_POINTS_ENABLED)
    except props.DoesNotExist:
        settings_prop = props()
        settings_prop.key = constants.OPPIA_POINTS_ENABLED
        if hasattr(settings, 'OPPIA_POINTS_ENABLED'):
            settings_prop.bool_value = settings.OPPIA_POINTS_ENABLED
        else:
            settings_prop.bool_value = True
        settings_prop.save()


def move_badges(props):
    try:
        props.objects.get(key=constants.OPPIA_BADGES_ENABLED)
    except props.DoesNotExist:
        settings_prop = props()
        settings_prop.key = constants.OPPIA_BADGES_ENABLED
        if hasattr(settings, 'OPPIA_BADGES_ENABLED'):
            settings_prop.bool_value = settings.OPPIA_BADGES_ENABLED
        else:
            settings_prop.bool_value = True
        settings_prop.save()


def move_ga(props):
    try:
        props.objects.get(key=constants.OPPIA_GOOGLE_ANALYTICS_ENABLED)
    except props.DoesNotExist:
        settings_prop = props()
        settings_prop.key = constants.OPPIA_GOOGLE_ANALYTICS_ENABLED
        if hasattr(settings, 'OPPIA_GOOGLE_ANALYTICS_ENABLED'):
            settings_prop.bool_value = settings.OPPIA_GOOGLE_ANALYTICS_ENABLED
        else:
            settings_prop.bool_value = False
        settings_prop.save()


def move_google_play(props):
    try:
        props.objects.get(key=constants.OPPIA_ANDROID_ON_GOOGLE_PLAY)
    except props.DoesNotExist:
        settings_prop = props()
        settings_prop.key = constants.OPPIA_ANDROID_ON_GOOGLE_PLAY
        if hasattr(settings, 'OPPIA_ANDROID_ON_GOOGLE_PLAY'):
            settings_prop.bool_value = settings.OPPIA_ANDROID_ON_GOOGLE_PLAY
        else:
            settings_prop.bool_value = False
        settings_prop.save()


def move_ga_code(props):
    try:
        props.objects.get(key=constants.OPPIA_GOOGLE_ANALYTICS_CODE)
    except props.DoesNotExist:
        settings_prop = props()
        settings_prop.key = constants.OPPIA_GOOGLE_ANALYTICS_CODE
        if hasattr(settings, 'OPPIA_GOOGLE_ANALYTICS_CODE'):
            settings_prop.str_value = settings.OPPIA_GOOGLE_ANALYTICS_CODE
        else:
            settings_prop.str_value = None
        settings_prop.save()


def move_ga_domain(props):
    try:
        props.objects.get(key=constants.OPPIA_GOOGLE_ANALYTICS_DOMAIN)
    except props.DoesNotExist:
        settings_prop = props()
        settings_prop.key = constants.OPPIA_GOOGLE_ANALYTICS_DOMAIN
        if hasattr(settings, 'OPPIA_GOOGLE_ANALYTICS_DOMAIN'):
            settings_prop.str_value = settings.OPPIA_GOOGLE_ANALYTICS_DOMAIN
        else:
            settings_prop.str_value = None
        settings_prop.save()


def move_packageid(props):
    try:
        props.objects.get(key=constants.OPPIA_ANDROID_PACKAGEID)
    except props.DoesNotExist:
        settings_prop = props()
        settings_prop.key = constants.OPPIA_ANDROID_PACKAGEID
        if hasattr(settings, 'OPPIA_ANDROID_PACKAGEID'):
            settings_prop.str_value = settings.OPPIA_ANDROID_PACKAGEID
        else:
            settings_prop.str_value = None
        settings_prop.save()


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0009_settingproperties_bool_value'),
    ]

    operations = [
        migrations.RunPython(move_to_settings),
    ]
