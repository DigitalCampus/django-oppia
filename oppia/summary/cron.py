# Interpreter deliberately excluded here - set it in your cron shell script.
# /usr/bin/env python

import time

from datetime import date



def update_summaries(last_tracker_pk=0, last_points_pk=0):

    from django.contrib.auth.models import User
    from django.db.models import Count

    from oppia.models import Tracker, Points, Course
    from oppia.settings.models import SettingProperties
    from oppia.summary.models import UserCourseSummary, CourseDailyStats, UserPointsSummary
    
    start = time.time()
    # get last tracker and points PKs to be processed
    # (to avoid leaving some out if new trackers arrive while processing)
    try:
        newest_tracker_pk = Tracker.objects.latest('id').id
        newest_points_pk = Points.objects.latest('id').id
    except Tracker.DoesNotExist:
        print "Tracker table is empty. Aborting cron..."
        return
    except Points.DoesNotExist:
        newest_points_pk = last_points_pk

    print ('Last tracker processed: %d\nNewest tracker: %d\n' % (last_tracker_pk, newest_tracker_pk))
    if last_tracker_pk >= newest_tracker_pk:
        print('No new trackers to process. Aborting cron...')
        return

    first_tracker = (last_tracker_pk == 0)
    first_points = (last_points_pk == 0)

    # If we are calculating from the start, delete previous summary calculations
    if first_tracker:
        UserCourseSummary.objects.all().delete()
        CourseDailyStats.objects.all().delete()
    if first_points:
        UserPointsSummary.objects.all().delete()

    # get different (distinct) user/courses involved
    userCourses = Tracker.objects \
        .filter(pk__gt=last_tracker_pk, pk__lte=newest_tracker_pk) \
        .exclude(course__isnull=True) \
        .values('course', 'user').distinct()

    totalUsers = userCourses.count()
    print ('%d different user/courses to process.' % totalUsers)

    count = 1
    for ucTracker in userCourses:
        print ('processing user/course trackers... (%d/%d)' % (count, totalUsers))
        print ucTracker
        user = User.objects.get(pk=ucTracker['user'])
        course = Course.objects.get(pk=ucTracker['course'])
        userCourse, created = UserCourseSummary.objects.get_or_create(course=course, user=user)
        userCourse.update_summary(
            last_tracker_pk=last_tracker_pk, last_points_pk=last_points_pk,
            newest_tracker_pk=newest_tracker_pk, newest_points_pk=newest_points_pk)
        count += 1

    # get different (distinct) courses/dates involved
    courseDailyTypeLogs = Tracker.objects \
        .filter(pk__gt=last_tracker_pk, pk__lte=newest_tracker_pk) \
        .exclude(course__isnull=True) \
        .extra({'day': "day(tracker_date)", 'month': "month(tracker_date)", 'year': "year(tracker_date)"}) \
        .values('course', 'day', 'month', 'year', 'type') \
        .annotate(total=Count('type')) \
        .order_by('day')

    totalLogs = courseDailyTypeLogs.count()
    print ('%d different courses/dates/types to process.' % totalLogs)
    count = 0
    for typeLog in courseDailyTypeLogs:
        day = date(typeLog['year'], typeLog['month'], typeLog['day'])
        course = Course.objects.get(pk=typeLog['course'])
        stats, created = CourseDailyStats.objects.get_or_create(course=course, day=day, type=typeLog['type'])
        stats.total = (0 if first_tracker else stats.total) + typeLog['total']
        stats.save()

        count += 1
        print count

    # get different (distinct) search logs involved
    searchDailyLogs = Tracker.objects \
        .filter(pk__gt=last_tracker_pk, pk__lte=newest_tracker_pk, user__is_staff=False, type='search') \
        .extra({'day': "day(tracker_date)", 'month': "month(tracker_date)", 'year': "year(tracker_date)"}) \
        .values('day', 'month', 'year') \
        .annotate(total=Count('id')) \
        .order_by('day')

    print ('%d different search/dates to process.' % searchDailyLogs.count())
    for searchLog in searchDailyLogs:
        day = date(searchLog['year'], searchLog['month'], searchLog['day'])
        stats, created = CourseDailyStats.objects.get_or_create(course=None, day=day, type='search')
        stats.total = (0 if first_tracker else stats.total) + searchLog['total']
        stats.save()

    # get different (distinct) user/points involved
    usersPoints = Points.objects \
        .filter(pk__gt=last_points_pk, pk__lte=newest_points_pk) \
        .values('user').distinct()

    totalUsers = usersPoints.count()
    print ('%d different user/points to process.' % totalUsers)
    for userPoints in usersPoints:
        user = User.objects.get(pk=userPoints['user'])
        points, created = UserPointsSummary.objects.get_or_create(user=user)
        points.update_points(last_points_pk=last_points_pk, newest_points_pk=newest_points_pk)

    # update last tracker and points PKs with the last one processed
    SettingProperties.objects.update_or_create(key='last_tracker_pk', defaults={"int_value": newest_tracker_pk})
    SettingProperties.objects.update_or_create(key='last_points_pk', defaults={"int_value": newest_points_pk})


def run():
    print 'Starting Oppia Summary cron...'
    start = time.time()

    from oppia.settings.models import SettingProperties
    
    # get last tracker and points PKs processed
    last_tracker_pk = SettingProperties.get_property('last_tracker_pk', 0)
    last_points_pk  = SettingProperties.get_property('last_points_pk', 0)

    update_summaries(last_tracker_pk, last_points_pk)

    elapsed_time = time.time() - start
    print ('cron completed, took %.2f seconds' % elapsed_time)

if __name__ == "__main__":
    import django
    django.setup()
    run()
