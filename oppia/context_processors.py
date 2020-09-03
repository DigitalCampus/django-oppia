# oppia/context_processors.py
import datetime
import oppia

from django.conf import settings
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
    version = "v" + str(oppia.VERSION[0]) + "." \
                + str(oppia.VERSION[1]) + "." \
                + str(oppia.VERSION[2]) + "-" \
                + str(oppia.VERSION[3]) + "." \
                + str(oppia.VERSION[4]) + "-" \
                + str(oppia.VERSION[5])
    return {'version': version}


def get_settings(request):
    self_register = SettingProperties.get_bool(
                                constants.OPPIA_ALLOW_SELF_REGISTRATION,
                                settings.OPPIA_ALLOW_SELF_REGISTRATION)

    show_gravatars = SettingProperties.get_bool(
                                constants.OPPIA_SHOW_GRAVATARS,
                                settings.OPPIA_SHOW_GRAVATARS)

    ga_enabled = SettingProperties.get_bool(
                                constants.OPPIA_GOOGLE_ANALYTICS_ENABLED,
                                settings.OPPIA_GOOGLE_ANALYTICS_ENABLED)

    ga_code = SettingProperties.get_string(
                                constants.OPPIA_GOOGLE_ANALYTICS_CODE,
                                settings.OPPIA_GOOGLE_ANALYTICS_CODE)

    ga_domain = SettingProperties.get_string(
                                constants.OPPIA_GOOGLE_ANALYTICS_DOMAIN,
                                settings.OPPIA_GOOGLE_ANALYTICS_DOMAIN)

    map_viz_enabled = SettingProperties.get_bool(
                                constants.OPPIA_MAP_VISUALISATION_ENABLED,
                                False)

    cron_warning = False
    last_cron = SettingProperties.get_string(
        constants.OPPIA_CRON_LAST_RUN, None)
    last_summary_cron = SettingProperties.get_string(
        constants.OPPIA_SUMMARY_CRON_LAST_RUN, None)

    TIME_ZONE_FIX = '+00:00'
    # fix for bad timezone dates
    if last_cron and TIME_ZONE_FIX not in last_cron:
        last_cron += TIME_ZONE_FIX

    if last_summary_cron and TIME_ZONE_FIX not in last_summary_cron:
        last_summary_cron += TIME_ZONE_FIX

    if last_cron is None or last_summary_cron is None:
        cron_warning = True
    else:
        start_date = datetime.datetime.now() - datetime.timedelta(days=7)
        last_cron_date = datetime.datetime.strptime(
            last_cron, constants.CRON_DATETIME_FORMAT)
        if last_cron_date < start_date:
            cron_warning = True

        last_summary_cron_date = datetime.datetime.strptime(
            last_summary_cron, constants.CRON_DATETIME_FORMAT)
        if last_summary_cron_date < start_date:
            cron_warning = True

    return {
        'OPPIA_ALLOW_SELF_REGISTRATION': self_register,
        'OPPIA_GOOGLE_ANALYTICS_ENABLED': ga_enabled,
        'OPPIA_GOOGLE_ANALYTICS_CODE': ga_code,
        'OPPIA_GOOGLE_ANALYTICS_DOMAIN': ga_domain,
        'OPPIA_SHOW_GRAVATARS': show_gravatars,
        'OPPIA_REPORTS': menu_reports(request),
        'DEBUG': settings.DEBUG,
        'CRON_WARNING': cron_warning,
        'OPPIA_MAP_VISUALISATION_ENABLED': map_viz_enabled}
