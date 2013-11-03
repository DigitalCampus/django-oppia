# oppia/signals.py
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import Signal

from oppia.models import Points, Award, Tracker, Activity, Section, Course, Cohort
from oppia.quiz.models import Quiz, QuizAttempt

import math

course_downloaded = Signal(providing_args=["course", "user"])

def signup_callback(sender, **kwargs):
    user = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        p = Points()
        p.points = settings.OPPIA_POINTS['REGISTER']
        p.type = 'signup'
        p.description = "Initial registration"
        p.user = user
        p.save()
    return

def quizattempt_callback(sender, **kwargs):
    quiz_attempt = kwargs.get('instance')
    
    # Check user doesn't own the quiz
    quiz = quiz_attempt.quiz
    if quiz.owner == quiz_attempt.user:
        return
    
    # give points to quiz owner
    if quiz_attempt.is_first_attempt_today() and not quiz.owner.is_superuser:
        p = Points()
        p.points = settings.OPPIA_POINTS['QUIZ_ATTEMPT_OWNER']
        p.user = quiz.owner
        p.type = 'userquizattempt'
        p.description = quiz_attempt.user.username + " attempted your quiz: " + quiz.title
        p.save() 
     
    # check not superuser
    if quiz_attempt.user.is_superuser:
        return 
    
    # find out if this quiz is part of a course
    course = None
    digest = quiz_attempt.get_quiz_digest()
    if digest is not None:
        # TODO - what are chances of 2 courses having the exact same activity? and what to do if they do?
        acts = Activity.objects.filter(digest=digest)
        for a in acts:
            course = a.section.course
        
    # find out is user is part of the cohort for this course
    cohort = None
    if course is not None:
        cohort = Cohort.student_member_now(course,quiz_attempt.user)
              
    if quiz_attempt.is_first_attempt():
        # If it's the first time they've attempted this quiz award points
        p = Points()
        p.points = settings.OPPIA_POINTS['QUIZ_FIRST_ATTEMPT']
        p.type = 'firstattempt'
        p.user = quiz_attempt.user
        p.description = "Bonus points for your first attempt at: " + quiz.title
        p.course = course
        p.cohort = cohort
        p.save()
    
        # add percentage points for their first attempt
        if quiz_attempt.get_score_percent() > 0:
            p = Points()
            p.points = quiz_attempt.get_score_percent()
            p.type = 'firstattemptscore'
            p.description = "Score for first attempt at quiz: " + quiz.title
            p.user = quiz_attempt.user
            p.course = course
            p.cohort = cohort
            p.save()
        
        # if you get 100% on first attempt get bonus of 50 points
        if quiz_attempt.get_score_percent() >= settings.OPPIA_POINTS['QUIZ_FIRST_ATTEMPT_THRESHOLD']:
            p = Points()
            p.points = settings.OPPIA_POINTS['QUIZ_FIRST_ATTEMPT_BONUS']
            p.type = 'firstattemptbonus'
            p.description = "Bonus points for getting 100% in first attempt at quiz: " + quiz.title
            p.user = quiz_attempt.user
            p.course = course
            p.cohort = cohort
            p.save()
            
    elif quiz_attempt.is_first_attempt_today():
        # If it's the first time today they've attempted this quiz award 10 points
        p = Points()
        p.points = settings.OPPIA_POINTS['QUIZ_ATTEMPT']
        p.type = 'quizattempt'
        p.user = quiz_attempt.user
        p.description = "Quiz attempt at: " + quiz.title
        p.course = course
        p.cohort = cohort
        p.save()
    
    return

def createquiz_callback(sender, **kwargs):
    quiz = kwargs.get('instance')
    created = kwargs.get('created')
    # check not superuser
    if quiz.owner.is_superuser:
        return 
    
    if created:
        p = Points()
        p.points = settings.OPPIA_POINTS['QUIZ_CREATED']
        p.type = 'quizcreated'
        p.description = "Quiz created: " + quiz.title
        p.user = quiz.owner
        p.save()
    return

def tracker_callback(sender, **kwargs):
    tracker = kwargs.get('instance')
    
    # check not superuser
    if tracker.user.is_superuser:
        return 
    
    if not tracker.activity_exists():
        return
    
    if tracker.get_activity_type() is not "media":
        if not tracker.is_first_tracker_today():
            return
        if not tracker.completed:
            return
    
    type = 'activitycompleted'
    points = settings.OPPIA_POINTS['ACTIVITY_COMPLETED']
    if tracker.get_activity_type() == "media":
        description =  "Media played: " + tracker.get_activity_title()
        type = 'mediaplayed'
        if tracker.is_first_tracker_today():
            points = settings.OPPIA_POINTS['MEDIA_STARTED']
        else:
            points = 0
        points =  (settings.OPPIA_POINTS['MEDIA_PLAYING_POINTS_PER_INTERVAL'] * math.floor(tracker.time_taken/settings.OPPIA_POINTS['MEDIA_PLAYING_INTERVAL']))
        if points > settings.OPPIA_POINTS['MEDIA_MAX_POINTS']:
            points = settings.OPPIA_POINTS['MEDIA_MAX_POINTS']
    else:
        description = "Activity completed: " + tracker.get_activity_title()    
       
    p = Points()
    p.points = points
    p.type = type
    p.description = description
    p.user = tracker.user
    p.course = tracker.course
    p.cohort = Cohort.student_member_now(tracker.course,tracker.user)
    p.save()
    
    # test if tracker submitted on time
    
    return

def course_download_callback(sender, **kwargs):
    user = kwargs.get('user')
    course = kwargs.get('course')
    
    # check not superuser
    if user.is_superuser:
        return 
    
    if not course.is_first_download(user):
        return 
    
    p = Points()
    p.points = settings.OPPIA_POINTS['COURSE_DOWNLOADED']
    p.type = 'coursedownloaded'
    p.description = "Course downloaded: " + course.get_title()
    p.user = user
    p.course = course
    p.cohort = Cohort.student_member_now(course,user)
    p.save()
    return

def badgeaward_callback(sender, **kwargs):
    award = kwargs.get('instance')
    
    # check not superuser
    if award.user.is_superuser:
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


