
import datetime
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from oppia.models import Course, Tracker

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