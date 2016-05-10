# Interpreter deliberately excluded here - set it in your cron shell script.
# /usr/bin/env python

import time

def run(hours):
    print 'Starting Oppia Summary cron...'
    start = time.time()

    #get last tracker and points PKs processed
    #get last tracker and points PKs to be processed
    # (to avoid leaving some out if new trackers arrive while processing)

    #get different (distinct) user/courses involved
    #for each user/course:
        #update userCourseSummary
        #userCourse, created = UserCourseSummary.objects.get_or_create(course=course, user=ser)
        #userCourse.update_summary(last_tracker_pk=ltpk, last_points_pk=lppk)

    #get different (distinct) courses/dates involved
        #update courseDailyStats

    #update last tracker and points PKs with the last one processed

    elapsed_time = time.time() - start
    print ('cron completed, took %.2f seconds' % elapsed_time)


if __name__ == "__main__":
    import django
    django.setup()
    run()
