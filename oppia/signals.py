import json
import math

from django.conf import settings
from django.db import models
from django.dispatch import Signal

from gamification.models import DefaultGamificationEvent
from oppia import DEFAULT_IP_ADDRESS
from oppia.models import Points, Tracker

from settings import constants
from settings.models import SettingProperties

course_downloaded = Signal(providing_args=["request", "course", "user"])

NON_ACTIVITY_EVENTS = [
    'course_downloaded', 'register'
]


def course_downloaded_callback(sender, **kwargs):
    request = kwargs.get('request')
    course = kwargs.get('course')

    tracker = Tracker()
    tracker.user = request.user
    tracker.course = course
    tracker.type = 'download'
    tracker.data = json.dumps({'version': course.version})
    tracker.ip = request.META.get('REMOTE_ADDR', DEFAULT_IP_ADDRESS)
    tracker.agent = request.META.get('HTTP_USER_AGENT', 'unknown')
    tracker.save()


# rules for applying points (or not)
def apply_points(user):
    if not SettingProperties.get_bool(
            constants.OPPIA_POINTS_ENABLED,
            settings.OPPIA_POINTS_ENABLED):
        return False
    if user.is_staff:
        return False
    return True


def calculate_media_points(tracker):
    if tracker.is_first_tracker_today():
        points = DefaultGamificationEvent.objects.get(
            event='media_started').points
    else:
        points = 0
    points += (DefaultGamificationEvent.objects.get(
        event='media_playing_points_per_interval').points
               * math.floor(tracker.time_taken
                            / DefaultGamificationEvent.objects
                            .get(
                                event='media_playing_interval')
                            .points))
    if points > DefaultGamificationEvent.objects.get(
      event='media_max_points').points:
        points = DefaultGamificationEvent.objects.get(
            event='media_max_points').points

    return points


def tracker_process_points(tracker, activity_type, description, points=None):
    if tracker.points is not None:
        points = tracker.points
        activity_type = tracker.event
        if not description:
            description = tracker.event
    else:
        if tracker.get_activity_type() != "media":
            if not tracker.is_first_tracker_today():
                return
            if not tracker.completed:
                return

    if points is None or points <= 0:
        return

    p = Points()
    p.points = points
    p.type = activity_type
    p.description = description
    p.user = tracker.user
    p.course = tracker.course
    p.save()


def tracker_callback(sender, **kwargs):

    tracker = kwargs.get('instance')
    description = None
    points = None
    activity_type = None

    if not apply_points(tracker.user):
        return

    if tracker.course is not None \
       and tracker.course.user == tracker.user:
        return

    if tracker.event not in NON_ACTIVITY_EVENTS \
            and tracker.activity_exists():

        activity_type = 'activity_completed'
        points = DefaultGamificationEvent.objects.get(
            event='activity_completed').points
        if tracker.get_activity_type() == "media":
            description = "Media played: " + tracker.get_activity_title()
            activity_type = 'mediaplayed'
            points = calculate_media_points(tracker)
        else:
            description = "Activity completed: " + tracker.get_activity_title()

    tracker_process_points(tracker, activity_type, description, points)


def badgeaward_callback(sender, **kwargs):
    award = kwargs.get('instance')
    if not apply_points(award.user):
        return

    p = Points()
    p.points = award.badge.points
    p.type = 'badgeawarded'
    p.description = award.description
    p.user = award.user
    p.save()


models.signals.post_save.connect(tracker_callback, sender=Tracker)
course_downloaded.connect(course_downloaded_callback)
