from django import template
from django.conf import settings

from settings.models import SettingProperties

register = template.Library()

ALLOWABLE_SETTING_VALUES = ("OPPIA_ANDROID_DEFAULT_PACKAGEID",
                            "BASESITE_URL",
                            "OPPIA_MAX_UPLOAD_SIZE")
ALLOWABLE_DB_SETTINGS = ("OPPIA_ANDROID_PACKAGEID",
                         "OPPIA_ANDROID_ON_GOOGLE_PLAY", "OPPIA_HOSTNAME")


# settings value (based on https://stackoverflow.com/a/21593607)
@register.simple_tag
def settings_value(name):
    if name in ALLOWABLE_SETTING_VALUES:
        return getattr(settings, name, '')
    if name in ALLOWABLE_DB_SETTINGS:
        return SettingProperties.get_property(name, None)
    return ''
