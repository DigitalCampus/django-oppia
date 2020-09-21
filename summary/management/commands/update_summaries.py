import time

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from django.utils import timezone

from oppia.models import Tracker, Points, Course
from settings.models import SettingProperties
from summary.models import UserCourseSummary, \
    CourseDailyStats, \
    UserPointsSummary

class Command(BaseCommand):
    help = 'Updates course and points summary tables'

    def add_arguments(self, parser):

        # Optional argument to start the summary calculation from the beginning
        parser.add_argument(
            '--fromstart',
            action='store_true',
            dest='fromstart',
            help='Calculate summary tables from the beginning, \
                  not just the last ones',
        )

    def handle(self, *args, **options):
        if options['fromstart']:
            self.update_summaries(0, 0)
        else:
            # get last tracker and points PKs processed
            last_tracker_pk = SettingProperties \
                .get_property('last_tracker_pk', 0)
            last_points_pk = SettingProperties \
                .get_property('last_points_pk', 0)
            self.update_summaries(last_tracker_pk, last_points_pk)
            
    def update_summaries(self, last_tracker_pk=0, last_points_pk=0):

        # check if cron already running
        prop, created = SettingProperties.objects \
            .get_or_create(key='oppia_summary_cron_lock',
                           int_value=1)
        if not created:
            print("Oppia summary cron is already running")
            return
    
        try:
            SettingProperties.objects.get(key='oppia_cron_lock')
            print("Oppia cron is already running")
            SettingProperties.delete_key('oppia_summary_cron_lock')
            return
        except SettingProperties.DoesNotExist:
            # do nothing
            pass
    
        SettingProperties.set_string('oppia_summary_cron_last_run',
                                     timezone.now())
    
        # get last tracker and points PKs to be processed
        # (to avoid leaving some out if new trackers arrive while processing)
        try:
            newest_tracker_pk = Tracker.objects.latest('id').id
            newest_points_pk = Points.objects.latest('id').id
        except Tracker.DoesNotExist:
            print("Tracker table is empty. Aborting cron...")
            SettingProperties.delete_key('oppia_summary_cron_lock')
            return
        except Points.DoesNotExist:
            newest_points_pk = last_points_pk
    
        print('Last tracker processed: %d\nNewest tracker: %d\n'
              % (last_tracker_pk,
                 newest_tracker_pk))
        if last_tracker_pk >= newest_tracker_pk:
            print('No new trackers to process. Aborting cron...')
            SettingProperties.delete_key('oppia_summary_cron_lock')
            return
    
        first_tracker = (last_tracker_pk == 0)
        first_points = (last_points_pk == 0)
    
        # If we are calculating from the start, delete previous summary
        # calculations
        if first_tracker:
            UserCourseSummary.objects.all().delete()
            CourseDailyStats.objects.all().delete()
        if first_points:
            UserPointsSummary.objects.all().delete()
    
        # get different (distinct) user/courses involved
        user_courses = Tracker.objects \
            .filter(pk__gt=last_tracker_pk, pk__lte=newest_tracker_pk) \
            .exclude(course__isnull=True) \
            .values('course', 'user').distinct()
    
        total_users = user_courses.count()
        print('%d different user/courses to process.' % total_users)
    
        count = 1
        for uc_tracker in user_courses:
            print('processing user/course trackers... (%d/%d)' % (count,
                                                                  total_users))
            user = User.objects.get(pk=uc_tracker['user'])
            course = Course.objects.get(pk=uc_tracker['course'])
            user_course, created = UserCourseSummary.objects \
                .get_or_create(course=course, user=user)
            user_course.update_summary(
                last_tracker_pk=last_tracker_pk,
                last_points_pk=last_points_pk,
                newest_tracker_pk=newest_tracker_pk,
                newest_points_pk=newest_points_pk)
            count += 1
    
        # get different (distinct) courses/dates involved
        course_daily_type_logs = Tracker.objects \
            .filter(pk__gt=last_tracker_pk, pk__lte=newest_tracker_pk) \
            .exclude(course__isnull=True) \
            .annotate(day=TruncDay('tracker_date'),
                      month=TruncMonth('tracker_date'),
                      year=TruncYear('tracker_date')) \
            .values('course', 'day', 'month', 'year', 'type') \
            .annotate(total=Count('type')) \
            .order_by('day')
    
        total_logs = course_daily_type_logs.count()
        print('%d different courses/dates/types to process.' % total_logs)
        count = 0
        for type_log in course_daily_type_logs:
            course = Course.objects.get(pk=type_log['course'])
            stats, created = CourseDailyStats.objects \
                .get_or_create(course=course,
                               day=type_log['day'],
                               type=type_log['type'])
            stats.total = (0 if first_tracker else stats.total) + type_log['total']
            stats.save()
    
            count += 1
            print(count)
    
        # get different (distinct) search logs involved
        search_daily_logs = Tracker.objects \
            .filter(pk__gt=last_tracker_pk,
                    pk__lte=newest_tracker_pk,
                    user__is_staff=False,
                    type='search') \
            .annotate(day=TruncDay('tracker_date'),
                      month=TruncMonth('tracker_date'),
                      year=TruncYear('tracker_date')) \
            .values('day', 'month', 'year') \
            .annotate(total=Count('id')) \
            .order_by('day')
    
        print('%d different search/dates to process.' % search_daily_logs.count())
        for search_log in search_daily_logs:
            stats, created = CourseDailyStats.objects \
                .get_or_create(course=None,
                               day=search_log['day'],
                               type='search')
            stats.total = (0 if first_tracker else stats.total) \
                + search_log['total']
            stats.save()
    
        # get different (distinct) user/points involved
        users_points = Points.objects \
            .filter(pk__gt=last_points_pk, pk__lte=newest_points_pk) \
            .values('user').distinct()
    
        total_users = users_points.count()
        print('%d different user/points to process.' % total_users)
        for user_points in users_points:
            user = User.objects.get(pk=user_points['user'])
            points, created = UserPointsSummary.objects.get_or_create(user=user)
            points.update_points(last_points_pk=last_points_pk,
                                 newest_points_pk=newest_points_pk)
    
        # update last tracker and points PKs with the last one processed
        SettingProperties.objects.update_or_create(key='last_tracker_pk',
                                                   defaults={"int_value":
                                                             newest_tracker_pk})
        SettingProperties.objects.update_or_create(key='last_points_pk',
                                                   defaults={"int_value":
                                                             newest_points_pk})
    
        SettingProperties.delete_key('oppia_summary_cron_lock')
