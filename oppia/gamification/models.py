# oppia/gamification/models.py
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from oppia.models import Course, Activity, Media
from oppia.quiz.models import Quiz 

class CourseGamificationEvent(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    created_date = models.DateTimeField('date created',default=timezone.now)
    event = models.CharField(max_length=100)
    points = models.IntegerField()
    
    class Meta:
        verbose_name = _(u'Course Gamification Event')
        verbose_name_plural = _(u'Course Gamification Events')
        
    def __unicode__(self):
        return self.event
    
class ActivityGamificationEvent(models.Model):
    user = models.ForeignKey(User)
    activity = models.ForeignKey(Activity)
    created_date = models.DateTimeField('date created',default=timezone.now)
    event = models.CharField(max_length=100)
    points = models.IntegerField()
    
    class Meta:
        verbose_name = _(u'Activity Gamification Event')
        verbose_name_plural = _(u'Activity Gamification Events')
        
    def __unicode__(self):
        return self.event
    
class MediaGamificationEvent(models.Model):
    user = models.ForeignKey(User)
    media = models.ForeignKey(Media)
    created_date = models.DateTimeField('date created',default=timezone.now)
    event = models.CharField(max_length=100)
    points = models.IntegerField()
    
    class Meta:
        verbose_name = _(u'Media Gamification Event')
        verbose_name_plural = _(u'Media Gamification Events')
        
    def __unicode__(self):
        return self.event
    
class QuizGamificationEvent(models.Model):
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz)
    created_date = models.DateTimeField('date created',default=timezone.now)
    event = models.CharField(max_length=100)
    points = models.IntegerField()
    
    class Meta:
        verbose_name = _(u'Quiz Gamification Event')
        verbose_name_plural = _(u'Quiz Gamification Events')
        
    def __unicode__(self):
        return self.event