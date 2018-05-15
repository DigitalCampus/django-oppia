# oppia/gamification/models.py
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from oppia.models import Course, Activity, Media
from oppia.quiz.models import Quiz 

class CourseGamificationPoints(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    created_date = models.DateTimeField('date created',default=timezone.now)
    points_type = models.CharField(max_length=100)
    points = models.IntegerField()
    
    class Meta:
        verbose_name = _(u'Course Gamification Points')
        verbose_name_plural = _(u'Course Gamification Points')
        
    def __unicode__(self):
        return self.points_type
    
class ActivityGamificationPoints(models.Model):
    user = models.ForeignKey(User)
    activity = models.ForeignKey(Activity)
    created_date = models.DateTimeField('date created',default=timezone.now)
    points_type = models.CharField(max_length=100)
    points = models.IntegerField()
    
    class Meta:
        verbose_name = _(u'Activity Gamification Points')
        verbose_name_plural = _(u'Activity Gamification Points')
        
    def __unicode__(self):
        return self.points_type
    
class MediaGamificationPoints(models.Model):
    user = models.ForeignKey(User)
    media = models.ForeignKey(Media)
    created_date = models.DateTimeField('date created',default=timezone.now)
    points_type = models.CharField(max_length=100)
    points = models.IntegerField()
    
    class Meta:
        verbose_name = _(u'Media Gamification Points')
        verbose_name_plural = _(u'Media Gamification Points')
        
    def __unicode__(self):
        return self.points_type
    
class QuizGamificationPoints(models.Model):
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz)
    created_date = models.DateTimeField('date created',default=timezone.now)
    points_type = models.CharField(max_length=100)
    points = models.IntegerField()
    
    class Meta:
        verbose_name = _(u'Quiz Gamification Points')
        verbose_name_plural = _(u'Quiz Gamification Points')
        
    def __unicode__(self):
        return self.points_type