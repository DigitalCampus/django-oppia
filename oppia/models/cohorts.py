
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from oppia.models import Course, Award


class Cohort(models.Model):
    description = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('Cohort')
        verbose_name_plural = _('Cohorts')

    def __unicode__(self):
        return self.description

    def no_student_members(self):
        return Participant.objects.filter(cohort=self, role=Participant.STUDENT).count()

    def no_teacher_members(self):
        return Participant.objects.filter(cohort=self, role=Participant.TEACHER).count()

    def get_courses(self):
        courses = Course.objects.filter(coursecohort__cohort=self).order_by('title')
        return courses

    def get_leaderboard(self, count=0):
        users = User.objects.filter(participant__cohort=self,
                                    participant__role=Participant.STUDENT,
                                    points__course__coursecohort__cohort=self) \
            .annotate(total=Sum('points__points')) \
            .order_by('-total')

        if count != 0:
            users = users[:count]

        for u in users:
            u.badges = Award.objects.filter(user=u, awardcourse__course__coursecohort__cohort=self).count()
            if u.total is None:
                u.total = 0
        return users


class CourseCohort(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("course", "cohort")


class Participant(models.Model):
    TEACHER = 'teacher'
    STUDENT = 'student'
    ROLE_TYPES = (
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    )
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_TYPES)

    class Meta:
        verbose_name = _('Participant')
        verbose_name_plural = _('Participants')
