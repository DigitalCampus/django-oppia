# oppia/gamification/models.py
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from oppia.models import Course, Activity, Media
from quiz.models import Quiz


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


class QuizGamificationEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created_date = models.DateTimeField('date created', default=timezone.now)
    event = models.CharField(max_length=100)
    points = models.IntegerField()

    class Meta:
        verbose_name = _(u'Quiz Gamification Event')
        verbose_name_plural = _(u'Quiz Gamification Events')

    def __unicode__(self):
        return self.event
