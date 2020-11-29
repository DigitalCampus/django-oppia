import datetime

from django.db.utils import IntegrityError
from django.utils import timezone

from oppia.models import Tracker

from summary.models import CourseDailyStats


def update_course_daily_stats_dates():
    start_date = timezone.now()
    cdss = CourseDailyStats.objects.all()
    for cds in cdss:
        try:
            minus_days = cds.id % 31
            new_date = start_date - datetime.timedelta(minus_days)
            cds.day = new_date
            cds.save()
        except IntegrityError:
            pass


def update_tracker_dates():
    start_date = timezone.now()
    trackers = Tracker.objects.all()
    for tracker in trackers:
        try:
            minus_days = tracker.id % 31
            new_date = start_date - datetime.timedelta(minus_days)
            tracker.submitted_date = new_date
            tracker.tracker_date = new_date
            tracker.save()
        except IntegrityError:
            pass
