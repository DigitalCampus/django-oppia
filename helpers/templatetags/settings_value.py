from django import template
from django.conf import settings

register = template.Library()

ALLOWABLE_VALUES = ("OPPIA_ANDROID_PACKAGEID", "OPPIA_ANDROID_ON_GOOGLE_PLAY", "OPPIA_ANDROID_DEFAULT_PACKAGEID", "BASESITE_URL", "OPPIA_MAX_UPLOAD_SIZE")

# settings value (based on https://stackoverflow.com/a/21593607)
@register.simple_tag
def settings_value(name):
    if name in ALLOWABLE_VALUES:
        return getattr(settings, name, '')
    return ''
