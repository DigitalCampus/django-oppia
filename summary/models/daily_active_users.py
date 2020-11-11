import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Count
from django.utils.translation import ugettext_lazy as _


class DailyActiveUsers(models.Model):
    day = models.DateField(blank=False,
                           null=False)
    total_submitted_date = models.IntegerField(blank=False,
                                null=False,
                                default=0)
    total_tracker_date = models.IntegerField(blank=False,
                                null=False,
                                default=0)

    class Meta:
        verbose_name = _(u'DailyActiveUsers')
        verbose_name_plural = _(u'DailyActiveUsers')
        unique_together = ("day", "total_submitted_date")
        index_together = ["day", "total_submitted_date"]

    def get_total_time_spent(self):
        summary_count_time_total = DailyActiveUser.objects.filter(
            dau=self, user__is_staff=False) \
            .aggregate(total_time=Sum('time_spent'))
        time_spent = 0
        if summary_count_time_total['total_time']:
            time_spent = summary_count_time_total['total_time']
        return time_spent


class DailyActiveUser(models.Model):
    SUBMITTED = 'submitted'
    TRACKER = 'tracker'
    DATE_TYPES = (
        (SUBMITTED, 'submitted'),
        (TRACKER, 'tracker')
    )

    dau = models.ForeignKey(DailyActiveUsers,
                            on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=DATE_TYPES)
    time_spent = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = _(u'DailyActiveUser')
        verbose_name_plural = _(u'DailyActiveUsers')
        unique_together = ("dau", "user", "type")
