# oppia/signals.py
import warnings

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import Signal

from oppia.gamification.default_points import OPPIA_DEFAULT_POINTS
from oppia.models import Points, Award, Tracker, Activity, Section, Course, Cohort
from oppia.quiz.models import Quiz, QuizAttempt
from oppia.utils.deprecation import RemovedInOppia0110Warning

import math

course_downloaded = Signal(providing_args=["course", "user"])


# rules for applying points (or not)
def apply_points(user):
    if not settings.OPPIA_POINTS_ENABLED:
        return False
    if user.is_staff and not settings.OPPIA_STAFF_EARN_POINTS:
        return False
    return True

        
def signup_callback(sender, **kwargs):

    user = kwargs.get('instance')
    created = kwargs.get('created')
    if not apply_points(user):
        return

    if created:
        p = Points()
        p.points = OPPIA_DEFAULT_POINTS['REGISTER']
        p.type = 'signup'
        p.description = "Initial registration"
        p.user = user
        p.save()
    return


def quizattempt_callback(sender, **kwargs):
    quiz_attempt = kwargs.get('instance')

    quiz = quiz_attempt.quiz

    # find out if this quiz is part of a course
    course = None
    digest = quiz_attempt.get_quiz_digest()
    if digest is not None:
        # TODO - what are chances of 2 courses having the exact same activity? and what to do if they do?
        acts = Activity.objects.filter(digest=digest)
        for a in acts:
            course = a.section.course

    if quiz_attempt.points is not None:
        p = Points()
        p.points = quiz_attempt.points
        p.type = 'quiz_attempt'
        p.user = quiz_attempt.user
        p.description = quiz_attempt.event
        p.course = course
        p.save()
        return

    # Check user doesn't own the quiz
    if quiz.owner == quiz_attempt.user:
        return

    if not apply_points(quiz_attempt.user):
        return

    # find out is user is part of the cohort for this course
    if course is not None and course.user == quiz_attempt.user and settings.OPPIA_COURSE_OWNERS_EARN_POINTS is False:
        return
     
    if quiz_attempt.is_first_attempt():
        # If it's the first time they've attempted this quiz award points
        p = Points()
        p.points = OPPIA_DEFAULT_POINTS['QUIZ_FIRST_ATTEMPT']
        p.type = 'firstattempt'
        p.user = quiz_attempt.user
        p.description = "Bonus points for your first attempt at: " + quiz.title
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
        if quiz_attempt.get_score_percent() >= OPPIA_DEFAULT_POINTS['QUIZ_FIRST_ATTEMPT_THRESHOLD']:
            p = Points()
            p.points = OPPIA_DEFAULT_POINTS['QUIZ_FIRST_ATTEMPT_BONUS']
            p.type = 'firstattemptbonus'
            p.description = "Bonus points for getting 100% in first attempt at quiz: " + quiz.title
            p.user = quiz_attempt.user
            p.course = course
            p.save()

    elif quiz_attempt.is_first_attempt_today():
        # If it's the first time today they've attempted this quiz award 10 points
        p = Points()
        p.points = OPPIA_DEFAULT_POINTS['QUIZ_ATTEMPT']
        p.type = 'quizattempt'
        p.user = quiz_attempt.user
        p.description = "Quiz attempt at: " + quiz.title
        p.course = course
        p.save()

    return


def createquiz_callback(sender, **kwargs):
    warnings.warn(
        "oppia.signals.createquiz_callback() is deprecated and will be removed in Oppia server 0.11.0.",
        RemovedInOppia0110Warning, 2)
    quiz = kwargs.get('instance')
    created = kwargs.get('created')

    if not apply_points(quiz.owner):
        return

    if created:
        p = Points()
        p.points = OPPIA_DEFAULT_POINTS['QUIZ_CREATED']
        p.type = 'quizcreated'
        p.description = "Quiz created: " + quiz.title
        p.user = quiz.owner
        p.save()
    return


def tracker_callback(sender, **kwargs):

    tracker = kwargs.get('instance')

    if not apply_points(tracker.user):
        return

    if not tracker.activity_exists():
        return

    if tracker.course is not None and tracker.course.user == tracker.user and settings.OPPIA_COURSE_OWNERS_EARN_POINTS is False:
        return

    type = 'activity_completed'
    points = OPPIA_DEFAULT_POINTS['ACTIVITY_COMPLETED']
    if tracker.get_activity_type() == "media":
        description = "Media played: " + tracker.get_activity_title()
        type = 'mediaplayed'
        if tracker.is_first_tracker_today():
            points = OPPIA_DEFAULT_POINTS['MEDIA_STARTED']
        else:
            points = 0
        points += (OPPIA_DEFAULT_POINTS['MEDIA_PLAYING_POINTS_PER_INTERVAL'] * math.floor(tracker.time_taken / OPPIA_DEFAULT_POINTS['MEDIA_PLAYING_INTERVAL']))
        if points > OPPIA_DEFAULT_POINTS['MEDIA_MAX_POINTS']:
            points = OPPIA_DEFAULT_POINTS['MEDIA_MAX_POINTS']
    else:
        description = "Activity completed: " + tracker.get_activity_title()

    if tracker.points is not None:
        points = tracker.points
        type = tracker.event
    else:
        if tracker.get_activity_type() is not "media":
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

    return


def course_download_callback(sender, **kwargs):
    warnings.warn(
        "oppia.signals.course_download_callback() is deprecated and will be removed in Oppia server 0.11.0.",
        RemovedInOppia0110Warning, 2)
    user = kwargs.get('user')
    course = kwargs.get('course')
    if not apply_points(user):
        return

    if course.user == user and settings.OPPIA_COURSE_OWNERS_EARN_POINTS is False:
        return

    if not course.is_first_download(user):
        return

    p = Points()
    p.points = OPPIA_DEFAULT_POINTS['COURSE_DOWNLOADED']
    p.type = 'coursedownloaded'
    p.description = "Course downloaded: " + course.get_title()
    p.user = user
    p.course = course
    p.save()
    return


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
    return

course_downloaded.connect(course_download_callback)
models.signals.post_save.connect(tracker_callback, sender=Tracker)
models.signals.post_save.connect(signup_callback, sender=User)
models.signals.post_save.connect(createquiz_callback, sender=Quiz)
models.signals.post_save.connect(quizattempt_callback, sender=QuizAttempt)
