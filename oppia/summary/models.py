from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from oppia.models import Course


class UserCourseSummary (models.Model):
    user   = models.ForeignKey(User, blank=False, null=False)
    course = models.ForeignKey(Course, blank=False, null=False)

    points = models.IntegerField(blank=False, null=False, default=0)
    total_downloads = models.IntegerField(blank=False, null=False, default=0)
    total_activity  = models.IntegerField(blank=False, null=False, default=0)
    quizzes_passed  = models.IntegerField(blank=False, null=False, default=0)
    badges_achieved = models.IntegerField(blank=False, null=False, default=0)
    pretest_score   = models.FloatField(blank=False, null=False, default=0)
    media_viewed    = models.IntegerField(blank=False, null=False, default=0)
    completed_activities = models.IntegerField(blank=False, null=False, default=0)



class CourseDailyStats (models.Model):
    course = models.ForeignKey(Course, blank=False, null=False)
    day = models.DateField(blank=False, null=False)

    type = models.CharField(max_length=10,null=True, blank=True, default=None)
    total = models.IntegerField(blank=False, null=False, default=0)
    quizzes_passed  = models.IntegerField(blank=False, null=False, default=0)
    completed_activities = models.IntegerField(blank=False, null=False, default=0)
    media_viewed = models.IntegerField(blank=False, null=False, default=0)
    resources_viewed = models.IntegerField(blank=False, null=False, default=0)


