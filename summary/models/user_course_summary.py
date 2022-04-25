from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Count, QuerySet
from django.utils.translation import gettext_lazy as _

from oppia import constants
from oppia.models import Course, Tracker, Points, Award, Activity


class UserCourseSummaryQS(QuerySet):

    AGGREGABLE_STATS = ('total_downloads',
                        'total_activity',
                        'badges_achieved',
                        'media_viewed',
                        'completed_activities')

    def get_stats_summary(self, user, course):

        course_stats = UserCourseSummary.get_stats_dict(course)
        summary = UserCourseSummary.objects.filter(user=user, course=course).first()

        if summary:
            course_stats['no_quizzes_completed'] = summary.quizzes_passed
            course_stats['pretest_score'] = summary.pretest_score
            course_stats['no_activities_completed'] = summary.completed_activities
            course_stats['no_media_viewed'] = summary.media_viewed
            course_stats['no_points'] = summary.points
            course_stats['no_badges'] = summary.badges_achieved

        return course_stats

    def aggregated_stats(self, type, single=False):
        if type in self.AGGREGABLE_STATS:
            qs = self.exclude(user__userprofile__exclude_from_reporting=True)
            stats = list(qs.values('course').annotate(distinct=Count('user'), total=Sum(type)))
            if single:
                return stats[0] if len(stats) > 0 else None
            else:
                return stats


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
    total_activity_current = models.IntegerField(blank=False, null=False, default=0)
    total_activity_previous = models.IntegerField(blank=False, null=False, default=0)

    objects = UserCourseSummaryQS.as_manager()

    class Meta:
        verbose_name = _(u'UserCourseSummary')
        verbose_name_plural = _(u'UserCourseSummaries')
        unique_together = ("user", "course")
        index_together = ["user", "course"]

    @staticmethod
    def get_stats_dict(course):
        return {
            'course': course,
            'course_display': course.get_title(),
            'no_quizzes_completed': 0,
            'pretest_score': None,
            'no_activities_completed': 0,
            'no_media_viewed': 0,
            'no_points': 0,
            'no_badges': 0, }

    def update_summary(self,
                       last_tracker_pk=0, newest_tracker_pk=0,
                       # range of tracker ids to process
                       last_points_pk=0, newest_points_pk=0
                       # range of points ids to process
                       ):

        first_tracker = (last_tracker_pk == 0)
        first_points = (last_points_pk == 0)

        self_trackers = Tracker.objects.filter(user=self.user, course=self.course, pk__gt=last_tracker_pk, pk__lte=newest_tracker_pk)

        activity_trackers = self_trackers.exclude(type=constants.STR_TRACKER_TYPE_DOWNLOAD)

        # Add the values that are directly obtained from the last pks
        self.total_activity = (0 if first_tracker else self.total_activity) + activity_trackers.count()
        self.total_downloads = (0 if first_tracker else self.total_downloads)  + self_trackers.filter(
                type=constants.STR_TRACKER_TYPE_DOWNLOAD).count()

        filters = {
            'user': self.user,
            'course': self.course,
            'pk__gt': last_points_pk
        }
        if newest_points_pk > 0:
            filters['pk__lte'] = newest_points_pk
        new_points = Points.objects.filter(** filters) \
            .aggregate(total=Sum('points'))['total']

        if new_points:
            self.points = (0 if first_points else self.points) + new_points

        # Values that need to be recalculated (as the course digests may vary)
        self.pretest_score = Course.get_pre_test_score(self.course, self.user)
        self.quizzes_passed = Course.get_no_quizzes_completed(self.course, self.user)
        self.completed_activities = Course.get_activities_completed(self.course, self.user)
        self.media_viewed = Course.get_media_viewed(self.course, self.user)
        self.badges_achieved = Award.get_userawards(self.user, self.course)

        # Update the data in the database
        self.save()

        # update total_activity_current and total_activity_previous
        self.update_current_previous_activity()


    def update_current_previous_activity(self):
        # get the current activity digests
        # note: can't base only on the latest set of trackers since the values
        # could go up or down depending on current activities in the course,
        # some may have been removed or updated
        current_digests = Activity.objects.filter(
            section__course=self.course).values_list('digest', flat=True)

        current_activities = Tracker.objects.filter(
            user=self.user,
            course=self.course,
            digest__in=current_digests)

        self.total_activity_current = current_activities.count()
        self.total_activity_previous = self.total_activity \
            - self.total_activity_current
        # alternate approach for calculating total_activity_previous is to
        # actually inspect the trackers but this would take much longer
        self.save()
