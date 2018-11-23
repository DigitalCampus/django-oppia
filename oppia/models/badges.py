from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from oppia.models import Course


class Badge(models.Model):
    ref = models.CharField(max_length=20)
    name = models.TextField(blank=False)
    description = models.TextField(blank=True)
    default_icon = models.FileField(upload_to="badges")
    points = models.IntegerField(default=100)
    allow_multiple_awards = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Badge')
        verbose_name_plural = _('Badges')

    def __unicode__(self):
        return self.description


class Award(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=False)
    award_date = models.DateTimeField('date awarded', default=timezone.now)

    class Meta:
        verbose_name = _('Award')
        verbose_name_plural = _('Awards')

    def __unicode__(self):
        return self.description

    @staticmethod
    def get_userawards(user, course=None):
        awards = Award.objects.filter(user=user)
        if course is not None:
            awards = awards.filter(awardcourse__course=course)
        return awards.count()

    def _get_badge(self):
        badge_icon = self.badge.default_icon
        try:
            icon = AwardCourse.objects.get(award=self)
            if icon.course.badge_icon:
                return icon.course.badge_icon
        except AwardCourse.DoesNotExist:
            pass
        return badge_icon

    badge_icon = property(_get_badge)


class AwardCourse(models.Model):
    award = models.ForeignKey(Award, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_version = models.BigIntegerField(default=0)
