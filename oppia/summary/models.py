import time

import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Count
from django.utils.translation import ugettext_lazy as _

from oppia.models import Course, Tracker, Points


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
        self.badges_achieved = Course.get_badges(self.course, self.user)
        self.completed_activities = Course.get_activities_completed(self.course, self.user)

        ### Update the data in the database
        self.save()

        elapsed_time = time.time() - t
        print('took %.2f seconds' % elapsed_time)


class CourseDailyStats (models.Model):
    course = models.ForeignKey(Course, blank=True, null=True, default=None, on_delete=models.CASCADE)
    day = models.DateField(blank=False, null=False)
    type = models.CharField(max_length=10, null=True, blank=True, default=None)
    total = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        verbose_name = _('CourseDailyStats')
        unique_together = ("course", "day", "type")
        index_together = ["course", "day", "type"]

    @staticmethod
    def update_daily_summary(course, day, last_tracker_pk=0, newest_tracker_pk=0):  # range of tracker ids to process

        day_start = datetime.datetime.strptime(day.strftime("%Y-%m-%d") + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        day_end = datetime.datetime.strptime(day.strftime("%Y-%m-%d") + " 23:59:59", "%Y-%m-%d %H:%M:%S")

        course = Course.objects.get(pk=course)
        trackers = Tracker.objects.filter(course=course,
                                              tracker_date__gte=day_start, tracker_date__lte=day_end,
                                              pk__gt=last_tracker_pk, pk__lte=newest_tracker_pk) \
                                    .values('type').annotate(total=Count('type'))

        for type_stats in trackers:
            stats, created = CourseDailyStats.objects.get_or_create(course=course, day=day, type=type_stats['type'])
            stats.total = (0 if last_tracker_pk == 0 else stats.total) + type_stats['total']
            stats.save()


class UserPointsSummary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(blank=False, null=False, default=0)
    badges = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        verbose_name = _('UserPointsSummary')

    def update_points(self, last_points_pk=0, newest_points_pk=0):  # range of points ids to process

        first_points = (last_points_pk == 0)
        filters = {
            'pk__gt': last_points_pk,
            'user': self.user
        }
        if newest_points_pk > 0:
            filters['pk__lte'] = newest_points_pk

        new_points = Points.objects.filter( ** filters).aggregate(total=Sum('points'))['total']

        if not new_points:
            return

        # If we update the user points, we need to recalculate his badges as well
        badges = UserCourseSummary.objects.filter(user=self.user).aggregate(badges=Sum('badges_achieved'))['badges']
        self.badges = badges if badges else 0
        self.points = (0 if first_points else self.points) + new_points

        self.save()
