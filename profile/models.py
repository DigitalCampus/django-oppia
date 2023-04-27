
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from datarecovery.models import DataRecovery
from oppia.models import Participant, CoursePermissions


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True, null=True, default=None)
    can_upload = models.BooleanField(default=False)
    job_title = models.TextField(blank=True, null=True, default=None)
    organisation = models.TextField(blank=True, null=True, default=None)
    phone_number = models.TextField(blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    exclude_from_reporting = models.BooleanField(
        default=False,
        verbose_name=_('Exclude from reporting'),
        help_text=_('If checked, the activity from this user will not be taken into account for summary calculations '
                    'and reports'))

    def get_can_upload(self):
        if self.user.is_staff:
            return True
        manager = CoursePermissions.objects.filter(user=self.user, role=CoursePermissions.MANAGER)
        if manager.exists():
            return True
        return self.can_upload

    def get_can_upload_activitylog(self):
        return self.user.is_staff

    def is_student_only(self):
        if self.user.is_staff:
            return False
        teacher = Participant.objects.filter(user=self.user, role=Participant.TEACHER)
        manager = CoursePermissions.objects.filter(user=self.user, role=CoursePermissions.MANAGER)
        return not teacher.exists() and not manager.exists()

    def is_teacher_only(self):
        if self.user.is_staff:
            return False
        teacher = Participant.objects.filter(user=self.user, role=Participant.TEACHER)
        manager = CoursePermissions.objects.filter(user=self.user, role=CoursePermissions.MANAGER)
        return teacher.exists() and not manager.exists()

    def update_customfields(self, fields_dict):
        errors = []
        custom_fields = CustomField.objects.all()
        for custom_field in custom_fields:
            if custom_field.id in fields_dict and (
                (fields_dict[custom_field.id] != '' and fields_dict[custom_field.id] is not None)
                    or custom_field.required is True
            ):

                profile_field, created = UserProfileCustomField.objects \
                    .get_or_create(key_name=custom_field, user=self.user)

                if custom_field.type == 'int':
                    profile_field.value_int = fields_dict.get(custom_field.id, None)
                elif custom_field.type == 'bool':
                    profile_field.value_bool = fields_dict.get(custom_field.id, None)
                else:
                    profile_field.value_str = fields_dict.get(custom_field.id, None)

                profile_field.save()

        missing_fields = [field for field in fields_dict if field not in custom_fields.values_list('id',
                                                                                                   flat=True).all()]
        if missing_fields:
            errors.append(DataRecovery.Reason.CUSTOM_PROFILE_FIELDS_NOT_DEFINED_IN_THE_SERVER + str(missing_fields))

        return errors

    def get_customfields_dict(self):
        profile_fields = {}
        custom_fields = CustomField.objects.all()
        for custom_field in custom_fields:
            value = UserProfileCustomField.get_user_value(self.user, custom_field)
            if value is not None:
                profile_fields[custom_field.id] = value

        return profile_fields


class CustomField(models.Model):

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
    type = models.CharField(max_length=10, choices=DATA_TYPES, null=False, blank=False)
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

    @staticmethod
    def get_user_value(user, key_name):
        try:
            return UserProfileCustomField.objects.get(key_name=key_name, user=user).get_value()
        except UserProfileCustomField.DoesNotExist:
            return None

    def get_value(self):
        if self.value_bool is not None:
            return self.value_bool
        elif self.value_int is not None:
            return self.value_int
        else:
            return self.value_str
