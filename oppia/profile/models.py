# oppia/profile/models.py

from django.contrib.auth.models import User
from django.db import models

from oppia.models import Participant


class UserProfile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True, null=True, default=None)
    can_upload = models.BooleanField(default=False)
    job_title = models.TextField(blank=True, null=True, default=None)
    organisation = models.TextField(blank=True, null=True, default=None)
    phone_number = models.TextField(blank=True, null=True, default=None)

    def get_can_upload(self):
        if self.user.is_staff:
            return True
        return self.can_upload

    def get_can_upload_activitylog(self):
        if self.user.is_staff:
            return True
        return False

    def is_student_only(self):
        if self.user.is_staff:
            return False
        teach = Participant.objects.filter(user=self.user, role=Participant.TEACHER).count()
        if teach > 0:
            return False
        else:
            return True

    def is_teacher_only(self):
        if self.user.is_staff:
            return False
        teach = Participant.objects.filter(user=self.user, role=Participant.TEACHER).count()
        if teach > 0:
            return True
        else:
            return False
