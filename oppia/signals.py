import math

from django.conf import settings
from django.db import models
from django.dispatch import Signal

from gamification.models import DefaultGamificationEvent
from oppia.models import Points, Tracker, Activity

course_downloaded = Signal(providing_args=["course", "user"])

NON_ACTIVITY_EVENTS = [
    'course_downloaded', 'register'
]


# rules for applying points (or not)
def apply_points(user):
    if not settings.OPPIA_POINTS_ENABLED:
        return False
    if user.is_staff:
        return False
    return True


def quizattempt_callback(sender, **kwargs):
    quiz_attempt = kwargs.get('instance')

    quiz = quiz_attempt.quiz

    # find out if this quiz is part of a course
    course = None
    digest = quiz_attempt.get_quiz_digest()
    if digest is not None:
        # TODO - what are chances of 2 courses having the exact same activity?
        # and what to do if they do?
        acts = Activity.objects.filter(digest=digest)
        for a in acts:
            course = a.section.course

    # Check user doesn't own the quiz
    if quiz.owner == quiz_attempt.user:
        return

    if not apply_points(quiz_attempt.user):
        return

    # find out is user is part of the cohort for this course
    if course is not None \
            and course.user == quiz_attempt.user:
        return

    if quiz_attempt.is_first_attempt():
        # If it's the first time they've attempted this quiz award points
        p = Points()
        p.points = DefaultGamificationEvent.objects.get(
            event='quiz_first_attempt').points
        p.type = 'firstattempt'
        p.user = quiz_attempt.user
        p.description = "Bonus points for your first attempt at: " + \
            quiz.title
        p.course = course
        p.save()

        # add percentage points for their first attempt
        if quiz_attempt.get_score_percent() > 0:
            p = Points()
            p.points = quiz_attempt.get_score_percent()
            p.type = 'firstattemptscore'
            p.description = "Score for first attempt at quiz: " + quiz.title
            p.user = quiz_attempt.user
            p.course = course
            p.save()

        # if you get 100% on first attempt get bonus of 50 points
        if quiz_attempt.get_score_percent() \
           >= DefaultGamificationEvent.objects.get(
                event='quiz_first_attempt_threshold').points:
            p = Points()
            p.points = DefaultGamificationEvent.objects.get(
                event='quiz_first_attempt_bonus').points
            p.type = 'firstattemptbonus'
            p.description = "Bonus points for getting 100% in first attempt \
                             at quiz: " + quiz.title
            p.user = quiz_attempt.user
            p.course = course
            p.save()

    elif quiz_attempt.is_first_attempt_today():
        # If it's the first time today they've attempted this quiz award
        # 10 points
        p = Points()
        p.points = DefaultGamificationEvent.objects.get(
            event='quiz_attempt').points
        p.type = 'quizattempt'
        p.user = quiz_attempt.user
        p.description = "Quiz attempt at: " + quiz.title
        p.course = course
        p.save()


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


def tracker_process_points(tracker, type, description, points):
    if tracker.points is not None:
        points = tracker.points
        type = tracker.event
        if not description:
            description = tracker.event
    else:
        if tracker.get_activity_type() != "media":
            if not tracker.is_first_tracker_today():
                return
            if not tracker.completed:
                return

    p = Points()
    p.points = points
    p.type = type
    p.description = description
    p.user = tracker.user
    p.course = tracker.course
    p.save()


def tracker_callback(sender, **kwargs):

    tracker = kwargs.get('instance')
    description = None
    points = None
    type = None

    if not apply_points(tracker.user):
        return

    if tracker.course is not None \
       and tracker.course.user == tracker.user:
        return

    if tracker.event not in NON_ACTIVITY_EVENTS \
            and tracker.activity_exists():

        type = 'activity_completed'
        points = DefaultGamificationEvent.objects.get(
            event='activity_completed').points
        if tracker.get_activity_type() == "media":
            description = "Media played: " + tracker.get_activity_title()
            type = 'mediaplayed'
            points = calculate_media_points(tracker)
        else:
            description = "Activity completed: " + tracker.get_activity_title()

    tracker_process_points(tracker, type, description, points)


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
