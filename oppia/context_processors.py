# oppia/context_processors.py
from django.conf import settings

import oppia
from oppia.models import Points, Award
from reports.views import menu_reports
from settings import constants
from settings.models import SettingProperties

def get_points(request):
    if not request.user.is_authenticated:
        return {'points': 0, 'badges': 0}
    else:
        points = Points.get_userscore(request.user)
        if points is None:
            points = 0
        badges = Award.get_userawards(request.user)
        if badges is None:
            badges = 0
    return {'points': points, 'badges': badges}


def get_version(request):
    version = "v" + str(oppia.VERSION[0]) + "." + str(oppia.VERSION[1]) + "." + str(oppia.VERSION[2])
    return {'version': version}


def get_settings(request):
    self_register = SettingProperties.get_int(constants.OPPIA_ALLOW_SELF_REGISTRATION, settings.OPPIA_ALLOW_SELF_REGISTRATION)
    return {'OPPIA_ALLOW_SELF_REGISTRATION': self_register,
             'OPPIA_GOOGLE_ANALYTICS_ENABLED': settings.OPPIA_GOOGLE_ANALYTICS_ENABLED,
             'OPPIA_GOOGLE_ANALYTICS_CODE': settings.OPPIA_GOOGLE_ANALYTICS_CODE,
             'OPPIA_GOOGLE_ANALYTICS_DOMAIN': settings.OPPIA_GOOGLE_ANALYTICS_DOMAIN,
             'OPPIA_SHOW_GRAVATARS': settings.OPPIA_SHOW_GRAVATARS,
             'OPPIA_DEVICEADMIN_ENABLED': settings.DEVICE_ADMIN_ENABLED,
             'OPPIA_REPORTS': menu_reports(request),
             'DEBUG': settings.DEBUG, }
