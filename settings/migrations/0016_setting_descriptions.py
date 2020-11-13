# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.utils.translation import ugettext_lazy as _

from settings import constants


def add_setting_descriptions(apps, schema_editor):
    props = apps.get_model("settings", "SettingProperties")
    setting_oppia_data_retention_years_desc(props)
    setting_max_upload_size_desc(props)
    setting_oppia_allow_self_registration_desc(props)
    setting_oppia_android_on_google_play_desc(props)
    setting_oppia_android_packageid_desc(props)
    setting_oppia_badges_enabled_desc(props)
    setting_oppia_points_enabled_desc(props)
    setting_oppia_map_visualisation_enabled_desc(props)
    setting_oppia_cartodb_account_desc(props)
    setting_oppia_cartodb_key_desc(props)
    setting_oppia_google_analytics_code_desc(props)
    setting_oppia_google_analytics_domain_desc(props)
    setting_oppia_google_analytics_enabled_desc(props)
    setting_oppia_hostname_desc(props)
    setting_oppia_ipstack_apikey_desc(props)
    setting_oppia_show_gravatars_desc(props)


def setting_oppia_data_retention_years_desc(props):
    prop = props.objects.get(key=constants.OPPIA_DATA_RETENTION_YEARS)
    prop.description = _(u"The number of years for users data to be kept. \
        Any users who have not logged in and not had any tracker activity \
        in this number of years will be removed from Oppia, along with \
        their activity data")
    prop.save()


def setting_max_upload_size_desc(props):
    prop = props.objects.get(key=constants.MAX_UPLOAD_SIZE)
    prop.description = _(u"The maximum upload size, in bytes, of course \
        files that will be allowed")
    prop.save()


def setting_oppia_allow_self_registration_desc(props):
    prop = props.objects.get(key=constants.OPPIA_ALLOW_SELF_REGISTRATION)
    prop.description = _(u"Whether or not this Oppia server allows users \
        to self register")
    prop.save()


def setting_oppia_android_on_google_play_desc(props):
    prop = props.objects.get(key=constants.OPPIA_ANDROID_ON_GOOGLE_PLAY)
    prop.description = _(u"Whether or not this Oppia server has a specific \
        app available on the Google Play Store")
    prop.save()


def setting_oppia_android_packageid_desc(props):
    prop = props.objects.get(key=constants.OPPIA_ANDROID_PACKAGEID)
    prop.description = _(u"The java package id of the specific app on the \
        Google Play Store")
    prop.save()


def setting_oppia_badges_enabled_desc(props):
    prop = props.objects.get(key=constants.OPPIA_BADGES_ENABLED)
    prop.description = _(u"Whether or not badges are enabled for this \
        Oppia implementation")
    prop.save()


def setting_oppia_points_enabled_desc(props):
    prop = props.objects.get(key=constants.OPPIA_POINTS_ENABLED)
    prop.description = _(u"Whether or not points are enabled for this \
        Oppia implementation")
    prop.save()


def setting_oppia_map_visualisation_enabled_desc(props):
    prop = props.objects.get(key=constants.OPPIA_MAP_VISUALISATION_ENABLED)
    prop.description = _(u"Whether or not the map visualization is enabled \
        for this Oppia implementation")
    prop.save()


def setting_oppia_cartodb_account_desc(props):
    prop = props.objects.get(key=constants.OPPIA_CARTODB_ACCOUNT)
    prop.description = _(u"Username for the CartoDB account")
    prop.save()


def setting_oppia_cartodb_key_desc(props):
    prop = props.objects.get(key=constants.OPPIA_CARTODB_KEY)
    prop.description = _(u"CartoDB account API key")
    prop.save()


def setting_oppia_google_analytics_code_desc(props):
    prop = props.objects.get(key=constants.OPPIA_GOOGLE_ANALYTICS_CODE)
    prop.description = _(u"Google Analytics code, if enabled")
    prop.save()


def setting_oppia_google_analytics_domain_desc(props):
    prop = props.objects.get(key=constants.OPPIA_GOOGLE_ANALYTICS_DOMAIN)
    prop.description = _(u"Google Analytics domain name, if enabled")
    prop.save()


def setting_oppia_google_analytics_enabled_desc(props):
    prop = props.objects.get(key=constants.OPPIA_GOOGLE_ANALYTICS_ENABLED)
    prop.description = _(u"Whether or not Google Analytics is enabled")
    prop.save()


def setting_oppia_hostname_desc(props):
    prop = props.objects.get(key=constants.OPPIA_HOSTNAME)
    prop.description = _(u"Domain/hostname for this Oppia server")
    prop.save()


def setting_oppia_ipstack_apikey_desc(props):
    prop = props.objects.get(key=constants.OPPIA_IPSTACK_APIKEY)
    prop.description = _(u"IPStack API key")
    prop.save()


def setting_oppia_show_gravatars_desc(props):
    prop = props.objects.get(key=constants.OPPIA_SHOW_GRAVATARS)
    prop.description = _(u"Whether or not to use Gravatars for users' \
        profile pictures")
    prop.save()


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0015_data_retention_setting'),
    ]

    operations = [
        migrations.RunPython(add_setting_descriptions),
    ]
