# Interpreter deliberately excluded here - set it in your cron shell script.
# /usr/bin/env python

import time

from django.contrib.auth.models import User

from oppia.models import Tracker, Points, Course
from oppia.summary.models import SettingProperties, UserCourseSummary


def run():
    print 'Starting Oppia Summary cron...'
    start = time.time()

    #get last tracker and points PKs processed
    last_tracker_pk = SettingProperties.get_property('last_tracker_pk', 0)
    last_points_pk  = SettingProperties.get_property('last_points_pk', 0)

    #get last tracker and points PKs to be processed
    # (to avoid leaving some out if new trackers arrive while processing)
    newest_tracker_pk = Tracker.objects.latest('id').id
    newest_points_pk  = Points.objects.latest('id').id

    print ('Last tracker processed: %d\nNewest tracker: %d\n' % (last_tracker_pk, newest_tracker_pk))
    if last_tracker_pk >= newest_tracker_pk:
        print('No new trackers to process. Aborting cron...')
        return


    #get different (distinct) user/courses involved
    userCourses = Tracker.objects\
            .filter(pk__gt=last_tracker_pk, pk__lte=newest_tracker_pk)\
            .exclude(course__isnull=True)\
            .values('course','user').distinct()

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
        count+=1

    #get different (distinct) courses/dates involved
        #update courseDailyStats

    #update last tracker and points PKs with the last one processed
    SettingProperties.objects.update_or_create(key='last_tracker_pk', defaults={"int_value":newest_tracker_pk})
    SettingProperties.objects.update_or_create(key='last_points_pk', defaults={"int_value":newest_points_pk})

    elapsed_time = time.time() - start
    print ('cron completed, took %.2f seconds' % elapsed_time)


if __name__ == "__main__":
    import django
    django.setup()
    run()
