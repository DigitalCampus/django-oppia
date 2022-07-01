from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models


class DataRecovery(models.Model):

    class Type:
        ACTIVITY_LOG = 'activity_log'
        TRACKER = 'tracker'
        QUIZ = 'quiz'
        USER_PROFILE = 'user_profile'
        TYPE_CHOICES = [
            (ACTIVITY_LOG, 'Activity log'),
            (TRACKER, 'Tracker'),
            (QUIZ, 'Quiz'),
            (USER_PROFILE, 'User profile'),
        ]

    class Reason:
        DIFFERENT_TRACKER_SERVER = 'Different tracker server'
        NONE_OF_THE_INCLUDED_USERS_EXIST_ON_THE_SERVER = 'None of the included users exist on the server'
        USER_DID_NOT_EXIST_AND_WAS_CREATED = 'User did not exist previously on the server, and was created'
        MISSING_SERVER = 'Missing server'
        MISSING_ACTIVITY_DIGEST = 'Missing activity digest'
        MISSING_MEDIA_DIGEST = 'Missing media digest'
        MISSING_USER_TAG = 'Missing user tag'
        MISSING_TRACKERS_TAG = 'Missing trackers tag'
        MISSING_QUIZRESPONSES_TAG = 'Missing quizresponses tag'
        MISSING_COURSE_TAG = 'Missing course tag'
        QUESTION_DOES_NOT_EXIST = 'Question does not exist'
        QUESTION_FROM_DIFFERENT_QUIZ = 'Question from different quiz'
        QUIZ_DOES_NOT_EXIST = 'Quiz does not exist'
        JSON_DECODE_ERROR = 'JSON decode error'
        INAPPROPRIATE_ARGUMENT_VALUE = 'Inappropriate argument value'
        MAPPING_KEY_NOT_FOUND = 'Mapping key not found'
        INAPPROPRIATE_ARGUMENT_TYPE = 'Inappropriate argument type'
        CUSTOM_PROFILE_FIELDS_NOT_DEFINED_IN_THE_SERVER = 'Custom profile fields not defined in the server: '

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    data_type = models.CharField(choices=Type.TYPE_CHOICES, max_length=13, null=False, blank=False)
    reasons = models.CharField(max_length=500, null=True, blank=True)
    data = models.TextField(null=False, blank=False)
    recovered = models.BooleanField(default=False)

    @staticmethod
    def create_data_recovery_entry(user, data_type, reasons, data):
        DataRecovery.objects.create(user=user, data_type=data_type, reasons=','.join(reasons), data=data)
