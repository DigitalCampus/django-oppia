
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from oppia.models import Course

class UserCourseDailySummary(models.Model):
    day = models.DateField(blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, default=None)
    type = models.CharField(max_length=15, null=False, blank=False, verbose_name=_('Activity type'))

    time_spent_submitted = models.IntegerField(default=0)
    time_spent_tracked = models.IntegerField(default=0)

    total_submitted = models.IntegerField(blank=False, null=False, default=0)
    total_tracked = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        verbose_name = _(u'UserCourseDailySummary')
        verbose_name_plural = _(u'UserCourseDailySummaries')