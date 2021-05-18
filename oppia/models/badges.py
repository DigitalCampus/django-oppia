from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from oppia.models import Course


class BadgeMethod(models.Model):
    key = models.CharField(max_length=50, null=False, primary_key=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.key


class Badge(models.Model):
    ref = models.CharField(max_length=20)
    name = models.TextField(blank=False)
    description = models.TextField(blank=True)
    default_icon = models.FileField(upload_to="badges")
    points = models.IntegerField(default=100)
    allow_multiple_awards = models.BooleanField(default=False)
    default_method = models.ForeignKey(BadgeMethod,
                                       null=True,
                                       on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Badge')
        verbose_name_plural = _('Badges')

    def __str__(self):
        return self.description


class Award(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=False)
    award_date = models.DateTimeField('date awarded', default=timezone.now)
    certificate_pdf = models.FileField(upload_to="certificates/%Y/%m/",
                                       null=True,
                                       default=None)

    class Meta:
        verbose_name = _('Award')
        verbose_name_plural = _('Awards')

    def __str__(self):
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


class CertificateTemplate(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    image_file = models.FileField(
        upload_to="certificate/templates",
        help_text=_(u"We recommend a .png image of 842px by 595px"))

    include_name = models.BooleanField(default=True)
    include_date = models.BooleanField(default=True)
    include_course_title = models.BooleanField(default=True)

    name_x = models.IntegerField(default=0)
    name_y = models.IntegerField(default=0)

    date_x = models.IntegerField(default=0)
    date_y = models.IntegerField(default=0)

    course_title_x = models.IntegerField(default=0)
    course_title_y = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('Certificate Template')
        verbose_name_plural = _('Certificate Templates')

    def __str__(self):
        return self.badge.name + ": " + self.course.get_title()
