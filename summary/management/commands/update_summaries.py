import time

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from oppia import constants
from oppia.models import Tracker, Points, Course
from settings.models import SettingProperties
from summary.models import UserCourseSummary, CourseDailyStats, UserPointsSummary
from summary.models.user_course_daily_summary import UserCourseDailySummary


class Command(BaseCommand):
    help = _('Updates course, points and daily active users summary tables')
    MAX_TIME = 60*60*24

    def add_arguments(self, parser):

        # Optional argument to start the summary calculation from the beginning
        parser.add_argument('--fromstart',
                            action='store_true',
                            dest='fromstart',
                            help=_('Calculate summary tables from the beginning, not just the last ones'))

    def handle(self, *args, **options):

        # check if cron already running
        prop, created = SettingProperties.objects \
            .get_or_create(key='oppia_summary_cron_lock',
                           int_value=1)
        if not created:
            self.stdout.write(_("Oppia summary cron is already running"))
            return

        try:
            SettingProperties.objects.get(key='oppia_cron_lock')
            self.stdout.write(_("Oppia cron is already running"))
            SettingProperties.delete_key('oppia_summary_cron_lock')
            return
        except SettingProperties.DoesNotExist:
            # do nothing
            pass

        if options['fromstart']:
            self.update_summaries(0, 0)
        else:
            # get last tracker and points PKs processed
            last_tracker_pk = SettingProperties.get_property('last_tracker_pk', 0)
            last_points_pk = SettingProperties .get_property('last_points_pk', 0)
            self.update_summaries(last_tracker_pk, last_points_pk)

    def update_summaries(self, last_tracker_pk=0, last_points_pk=0):

        SettingProperties.set_string('oppia_summary_cron_last_run', timezone.now())

        # get last tracker and points PKs to be processed
        # (to avoid leaving some out if new trackers arrive while processing)
        try:
            newest_tracker_pk = Tracker.objects.latest('id').id
            newest_points_pk = Points.objects.latest('id').id
        except Tracker.DoesNotExist:
            self.stdout.write(_("Tracker table is empty. Aborting cron..."))
            SettingProperties.delete_key('oppia_summary_cron_lock')
            return
        except Points.DoesNotExist:
            newest_points_pk = last_points_pk

        print('Last tracker processed: %d\nNewest tracker: %d\n'
              % (last_tracker_pk, newest_tracker_pk))
        if last_tracker_pk >= newest_tracker_pk:
            self.stdout.write(_('No new trackers to process. Aborting cron...'))
            SettingProperties.delete_key('oppia_summary_cron_lock')
            return

        start_time = time.time()

        self.update_user_course_summary(last_tracker_pk, newest_tracker_pk, last_points_pk, newest_points_pk)
        self.update_course_daily_stats(last_tracker_pk, newest_tracker_pk)
        self.update_user_points_summary(last_points_pk, newest_points_pk)
        self.update_user_course_daily_stats(last_tracker_pk, newest_tracker_pk)

        print(_("--- took %s seconds ---") % (time.time() - start_time))

        # update last tracker and points PKs with the last one processed
        SettingProperties.objects.update_or_create(key='last_tracker_pk', defaults={"int_value": newest_tracker_pk})
        SettingProperties.objects.update_or_create(key='last_points_pk', defaults={"int_value": newest_points_pk})
        SettingProperties.delete_key('oppia_summary_cron_lock')

    # Updates the UserCourseSummary model
    def update_user_course_summary(self, last_tracker_pk=0, newest_tracker_pk=0, last_points_pk=0, newest_points_pk=0):

        if last_tracker_pk == 0:
            UserCourseSummary.objects.all().delete()

        user_courses = Tracker.objects \
            .filter(pk__gt=last_tracker_pk, pk__lte=newest_tracker_pk) \
            .exclude(course__isnull=True) \
            .exclude(type=constants.STR_TRACKER_TYPE_DOWNLOAD) \
            .values('course', 'user').distinct()

        total_users = user_courses.count()
        self.stdout.write(_('%d different user/courses to process.') % total_users)

        count = 1
        for uc_tracker in user_courses:
            self.stdout.write(_('processing user/course trackers... (%d/%d)') % (count, total_users))
            try:
                user = User.objects.get(pk=uc_tracker['user'])
            except User.DoesNotExist:
                continue
            course = Course.objects.get(pk=uc_tracker['course'])
            user_course, created = UserCourseSummary.objects.get_or_create(course=course, user=user)
            user_course.update_summary(
                last_tracker_pk=last_tracker_pk,
                last_points_pk=last_points_pk,
                newest_tracker_pk=newest_tracker_pk,
                newest_points_pk=newest_points_pk)
            count += 1

    # Updates the CourseDailyStats model
    def update_course_daily_stats(self, last_tracker_pk=0, newest_tracker_pk=0):

        if last_tracker_pk == 0:
            CourseDailyStats.objects.all().delete()

        excluded_users = UserCourseSummary.get_excluded_users()

        # get different (distinct) courses/dates involved
        course_daily_type_logs = Tracker.objects \
            .filter(pk__gt=last_tracker_pk, pk__lte=newest_tracker_pk) \
            .exclude(course__isnull=True) \
            .exclude(user__in=excluded_users) \
            .annotate(day=TruncDay('tracker_date')) \
            .values('course', 'day', 'type') \
            .annotate(total=Count('type')) \
            .order_by('day')

        total_logs = course_daily_type_logs.count()
        self.stdout.write(_('%d different courses/dates/types to process.') % total_logs)

        count = 0
        for type_log in course_daily_type_logs:
            course = Course.objects.get(pk=type_log['course'])
            stats, created = CourseDailyStats.objects.get_or_create(course=course,
                                                                    day=type_log['day'],
                                                                    type=type_log['type'])
            stats.total = (0 if last_tracker_pk == 0 else stats.total) + type_log['total']
            stats.save()

            count += 1
            self.stdout.write(str(count))

        # get different (distinct) non-course logs involved
        noncourse_types = ['search', 'login', 'register']

        noncourse_daily_logs = Tracker.objects \
            .filter(pk__gt=last_tracker_pk, pk__lte=newest_tracker_pk, type__in=noncourse_types) \
            .exclude(user__in=excluded_users) \
            .annotate(day=TruncDay('tracker_date')) \
            .values('day', 'type') \
            .annotate(total=Count('type')) \
            .order_by('day')

        self.stdout.write(_('%d different search/dates to process.') % noncourse_daily_logs.count())
        for log in noncourse_daily_logs:
            stats, created = CourseDailyStats.objects.get_or_create(course=None, day=log['day'], type=log['type'])
            stats.total += log['total']
            stats.save()

    # Updates the CourseDailyStats model
    def update_user_course_daily_stats(self, last_tracker_pk=0, newest_tracker_pk=0):
        if last_tracker_pk == 0:
            UserCourseDailySummary.objects.all().delete()

        self.update_daily_stats('tracker', 'tracked', last_tracker_pk, newest_tracker_pk)
        self.update_daily_stats('submitted', 'submitted', last_tracker_pk, newest_tracker_pk)

    def update_daily_stats(self, date_name, stats_name, last_tracker_pk=0, newest_tracker_pk=0):
        # get different (distinct) courses/dates involved
        daily_type_tracked = Tracker.objects \
            .filter(pk__gt=last_tracker_pk, pk__lte=newest_tracker_pk) \
            .exclude(course__isnull=True) \
            .annotate(day=TruncDay('{}_date'.format(date_name))) \
            .values('course', 'user', 'day', 'type') \
            .annotate(total=Count('type'), time_spent=Sum('time_taken')) \
            .order_by('day')

        total_logs = daily_type_tracked.count()
        self.stdout.write(_('{} different {} courses/dates/types to process.').format(total_logs, date_name))

        count = 1
        for log in daily_type_tracked:
            course = Course.objects.get(pk=log['course'])
            user = User.objects.get(pk=log['user'])
            print('{}/{}) {} {} - {} {}: {}'.format(count,
                                                    total_logs,
                                                    log['day'],
                                                    log['course'],
                                                    user.username,
                                                    log['type'],
                                                    log['total']))
            if log['type'] is None:
                print(_("Skipping as no value for tracker.type"))
                continue

            stats, created = UserCourseDailySummary.objects.get_or_create(
                day=log['day'], user=user, course=course, type=log['type'])

            total_field = 'total_{}'.format(stats_name)
            total = getattr(stats, total_field) + log['total']
            setattr(stats, total_field, total)

            time_spent_field = 'time_spent_{}'.format(stats_name)
            total = getattr(stats, time_spent_field) + log['time_spent']
            setattr(stats, time_spent_field, total)

            stats.save()
            count += 1

    # Updates the UserPointsSummary model
    def update_user_points_summary(self, last_points_pk=0, newest_points_pk=0):

        if last_points_pk == 0:
            UserPointsSummary.objects.all().delete()

        # get different (distinct) user/points involved
        users_points = Points.objects \
            .filter(pk__gt=last_points_pk, pk__lte=newest_points_pk) \
            .values('user').distinct()

        total_users = users_points.count()
        self.stdout.write(_('%d different user/points to process.') % total_users)
        for user_points in users_points:
            try:
                user = User.objects.get(pk=user_points['user'])
            except User.DoesNotExist:
                continue
            points, created = UserPointsSummary.objects.get_or_create(user=user)
            points.update_points(last_points_pk=last_points_pk, newest_points_pk=newest_points_pk)
