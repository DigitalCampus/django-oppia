
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from oppia.models import Course


class Tag(models.Model):
    name = models.TextField(blank=False)
    created_date = models.DateTimeField('date created', default=timezone.now)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    courses = models.ManyToManyField(Course, through='CourseTag')
    description = models.TextField(blank=True, null=True, default=None)
    order_priority = models.IntegerField(default=0)
    highlight = models.BooleanField(default=False)
    icon = models.FileField(upload_to="tags", null=True, blank=True, default=None)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __unicode__(self):
        return self.name


class CourseTag(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Course Tag')
        verbose_name_plural = _('Course Tags')
