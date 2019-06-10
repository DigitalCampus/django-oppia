# oppia/gamification/models.py
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from oppia.models import Course, Activity, Media
from quiz.models import Quiz


class DefaultGamificationEvent(models.Model):
    GLOBAL = 'global'
    COURSE = 'course'
    ACTIVITY = 'activity'
    QUIZ = 'quiz'
    MEDIA = 'media'
    LEVELS = (
        (GLOBAL, 'Global'),
        (COURSE, 'Course'),
        (ACTIVITY, 'Activity'),
        (QUIZ, 'Quiz'),
        (MEDIA, 'Media')
    )
    
    event = models.CharField(max_length=100)
    points = models.IntegerField()
    level = models.CharField(max_length=20, choices=LEVELS)
    label = models.CharField(max_length=100)
    helper_text = models.TextField(null=True, default=None)

    class Meta:
        verbose_name = _(u'Default Gamification Event')
        verbose_name_plural = _(u'Default Gamification Events')

    def __unicode__(self):
        return self.event
    
class CourseGamificationEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_date = models.DateTimeField('date created', default=timezone.now)
    event = models.CharField(max_length=100)
    points = models.IntegerField()

    class Meta:
        verbose_name = _(u'Course Gamification Event')
        verbose_name_plural = _(u'Course Gamification Events')

    def __unicode__(self):
        return self.event


class ActivityGamificationEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    created_date = models.DateTimeField('date created', default=timezone.now)
    event = models.CharField(max_length=100)
    points = models.IntegerField()

    class Meta:
        verbose_name = _(u'Activity Gamification Event')
        verbose_name_plural = _(u'Activity Gamification Events')

    def __unicode__(self):
        return self.event


class MediaGamificationEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    created_date = models.DateTimeField('date created', default=timezone.now)
    event = models.CharField(max_length=100)
    points = models.IntegerField()

    class Meta:
        verbose_name = _(u'Media Gamification Event')
        verbose_name_plural = _(u'Media Gamification Events')

    def __unicode__(self):
        return self.event

