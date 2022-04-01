# oppia/models/courselog.py

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from oppia.models.main import Course


class CoursePublishingLog(models.Model):

    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    new_version = models.BigIntegerField(null=True)
    old_version = models.BigIntegerField(null=True)
    log_date = models.DateTimeField('log_date', default=timezone.now)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    data = models.TextField(blank=False)

    class Meta:
        verbose_name = _('Course Publishing Log')
        verbose_name_plural = _('Course Publishing Logs')
