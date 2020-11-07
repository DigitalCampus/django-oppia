import datetime

from django.db import models
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