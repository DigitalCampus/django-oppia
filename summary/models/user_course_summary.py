import time

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from oppia.models import Course, Tracker, Points, Award


class UserCourseSummary (models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, blank=False, null=False, on_delete=models.CASCADE)

    points = models.IntegerField(blank=False, null=False, default=0)
    total_downloads = models.IntegerField(blank=False, null=False, default=0)
    total_activity = models.IntegerField(blank=False, null=False, default=0)
    quizzes_passed = models.IntegerField(blank=False, null=False, default=0)
    badges_achieved = models.IntegerField(blank=False, null=False, default=0)
    pretest_score = models.FloatField(blank=True, null=True)
    media_viewed = models.IntegerField(blank=False, null=False, default=0)
    completed_activities = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        verbose_name = _('UserCourseSummary')
        unique_together = ("user", "course")
        index_together = ["user", "course"]

    def update_summary(self,
                       last_tracker_pk=0, newest_tracker_pk=0,  # range of tracker ids to process
                       last_points_pk=0, newest_points_pk=0     # range of points ids to process
                       ):

        first_tracker = (last_tracker_pk == 0)
        first_points = (last_points_pk == 0)

        t = time.time()
        self_trackers = Tracker.objects.filter(user=self.user, course=self.course, pk__gt=last_tracker_pk, pk__lte=newest_tracker_pk)

        ### Add the values that are directly obtained from the last pks
        self.total_activity = (0 if first_tracker else self.total_activity) + self_trackers.count()
        self.total_downloads = (0 if first_tracker else self.total_downloads) + self_trackers.filter(type='download').count()

        filters = {
            'user': self.user,
            'course': self.course,
            'pk__gt': last_points_pk
        }
        if newest_points_pk > 0:
            filters['pk__lte'] = newest_points_pk
        new_points = Points.objects.filter( ** filters).aggregate(total=Sum('points'))['total']

        if new_points:
            self.points = (0 if first_points else self.points) + new_points

        ### Values that need to be recalculated (as the course digests may vary)
        self.pretest_score = Course.get_pre_test_score(self.course, self.user)
        self.quizzes_passed = Course.get_no_quizzes_completed(self.course, self.user)
        self.badges_achieved = Award.get_userawards(self.user, self.course)
        self.completed_activities = Course.get_activities_completed(self.course, self.user)
        self.media_viewed = Course.get_media_viewed(self.course, self.user)

        ### Update the data in the database
        self.save()

        elapsed_time = time.time() - t
        print('took %.2f seconds' % elapsed_time)
