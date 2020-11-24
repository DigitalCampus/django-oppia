# oppia/profile/models.py

from django.contrib.auth.models import User
from django.db import models

from oppia.models import Participant, CoursePermissions


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
        manager = CoursePermissions.objects \
            .filter(user=self.user,
                    role=CoursePermissions.MANAGER).count()
        if manager > 0:
            return True
        return self.can_upload

    def get_can_upload_activitylog(self):
        if self.user.is_staff:
            return True
        return False

    def is_student_only(self):
        if self.user.is_staff:
            return False
        teacher = Participant.objects.filter(user=self.user,
                                             role=Participant.TEACHER).count()
        manager = CoursePermissions.objects \
            .filter(user=self.user,
                    role=CoursePermissions.MANAGER).count()
        if teacher > 0 or manager > 0:
            return False
        else:
            return True

    def is_teacher_only(self):
        if self.user.is_staff:
            return False
        teacher = Participant.objects.filter(user=self.user,
                                             role=Participant.TEACHER).count()
        manager = CoursePermissions.objects \
            .filter(user=self.user,
                    role=CoursePermissions.MANAGER).count()
        if teacher > 0 and manager == 0:
            return True
        else:
            return False

    def update_customfields(self, fields_dict):

        custom_fields = CustomField.objects.all()
        for custom_field in custom_fields:
            if (custom_field.id in fields_dict
                and fields_dict[custom_field.id] != '') \
                    or custom_field.required is True:

                profile_field, created = UserProfileCustomField.objects \
                    .get_or_create(key_name=custom_field, user=self.user)

                if custom_field.type == 'int':
                    profile_field.value_int = fields_dict.get(custom_field.id,
                                                              None)
                elif custom_field.type == 'bool':
                    profile_field.value_bool = fields_dict.get(custom_field.id,
                                                               None)
                else:
                    profile_field.value_str = fields_dict.get(custom_field.id,
                                                              None)

                profile_field.save()


class CustomField (models.Model):

    DATA_TYPES = (
        ('str', 'String'),
        ('int', 'Integer'),
        ('bool', 'Boolean')
    )

    id = models.CharField(max_length=100, primary_key=True, editable=True)
    label = models.CharField(max_length=200, null=False, blank=False)
    required = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    helper_text = models.TextField(blank=True, null=True, default=None)
    type = models.CharField(max_length=10,
                            choices=DATA_TYPES,
                            null=False,
                            blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class UserProfileCustomField (models.Model):
    key_name = models.ForeignKey(CustomField, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value_str = models.TextField(blank=True, null=True, default=None)
    value_int = models.IntegerField(blank=True, null=True, default=None)
    value_bool = models.BooleanField(null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['key_name', 'user']

    def __str__(self):
        return self.key_name.id + ": " + self.user.username

    def get_value(self):
        if self.value_bool is not None:
            return self.value_bool
        elif self.value_int is not None:
            return self.value_int
        else:
            return self.value_str
