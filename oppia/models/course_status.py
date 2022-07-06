from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from oppia import constants


class CourseStatusManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

    def available_statuses(self):
        return self.filter(Q(available=True))


class CourseStatus(models.Model):
    LIVE = 'live'
    DRAFT = 'draft'
    ARCHIVED = 'archived'
    NEW_DOWNLOADS_DISABLED = 'new_downloads_disabled'
    READ_ONLY = 'read_only'
    COURSE_STATUS_CHOICES = [
        (LIVE, _('Live')),
        (DRAFT, _('Draft')),
        (ARCHIVED, _('Archived')),
        (NEW_DOWNLOADS_DISABLED, _('New downloads disabled')),
        (READ_ONLY, _('Read only')),
    ]

    name = models.CharField(primary_key=True,
                            max_length=100,
                            choices=COURSE_STATUS_CHOICES,
                            default=LIVE,
                            help_text=_(constants.STATUS_FIELD_HELP_TEXT))

    available = models.BooleanField(default=True)

    objects = CourseStatusManager()

    class Meta:
        verbose_name = _('Course Status')
        verbose_name_plural = _('Course Statuses')

    def __str__(self):
        return self.get_name_display()
