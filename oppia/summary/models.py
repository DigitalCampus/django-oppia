import time

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from oppia.models import Course, Tracker, Points


class UserCourseSummary (models.Model):
    user   = models.ForeignKey(User, blank=False, null=False)
    course = models.ForeignKey(Course, blank=False, null=False)

    points = models.IntegerField(blank=False, null=False, default=0)
    total_downloads = models.IntegerField(blank=False, null=False, default=0)
    total_activity  = models.IntegerField(blank=False, null=False, default=0)
    quizzes_passed  = models.IntegerField(blank=False, null=False, default=0)
    badges_achieved = models.IntegerField(blank=False, null=False, default=0)
    pretest_score   = models.FloatField(blank=True, null=True)
    media_viewed    = models.IntegerField(blank=False, null=False, default=0)
    completed_activities = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        verbose_name = _('UserCourseSummary')
        unique_together = ("user", "course")
        index_together  = ["user", "course"]


    def update_summary(self, last_tracker_pk=0, last_points_pk=0):

        ltpk = last_tracker_pk
        lppk = last_points_pk

        t = time.clock()
        selfTrackers = Tracker.objects.filter(user=self.user, course=self.course, pk__gt=last_tracker_pk)

        ### Add the values that are directly obtained from the last pks
        self.total_activity  = (0 if ltpk == 0 else self.total_activity) + selfTrackers.count()
        self.total_downloads = (0 if ltpk == 0 else self.total_activity) + selfTrackers.filter(type='download').count()
        new_points = Points.objects.filter(pk__gt=last_points_pk, course=self.course,user=self.user)\
                                     .aggregate(total=Sum('points'))['total']
        if new_points:
            self.points += (0 if lppk == 0 else self.points) + new_points
        ### Values that need to be recalculated (as the course digests may vary)
        self.pretest_score = Course.get_pre_test_score(self.course, self.user)
        self.quizzes_passed = Course.get_no_quizzes_completed(self.course, self.user)
        self.badges_achieved = Course.get_badges(self.course, self.user)
        self.completed_activities = Course.get_activities_completed(self.course, self.user)

        ### Update the data in the database
        self.save()

        elapsed_time = time.clock() - t
        print(self)
        print('took %.2f seconds' % elapsed_time)



class CourseDailyStats (models.Model):
    course = models.ForeignKey(Course, blank=False, null=False)
    day = models.DateField(blank=False, null=False)

    type = models.CharField(max_length=10,null=True, blank=True, default=None)
    total = models.IntegerField(blank=False, null=False, default=0)
    quizzes_passed  = models.IntegerField(blank=False, null=False, default=0)
    completed_activities = models.IntegerField(blank=False, null=False, default=0)
    media_viewed = models.IntegerField(blank=False, null=False, default=0)
    resources_viewed = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        verbose_name = _('CourseDailyStats')
        unique_together = ("course", "day")
        index_together  = ["course", "day"]
