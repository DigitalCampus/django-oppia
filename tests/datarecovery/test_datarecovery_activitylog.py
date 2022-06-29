import json

import os
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCaseMixin

from datarecovery.models import DataRecovery
from tests.utils import get_api_key


class ActivitylogUploadTest(ResourceTestCaseMixin, TestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_malaria_quiz.json',
                'tests/test_settings.json',
                'tests/test_permissions.json',
                'default_gamification_events.json']

    activity_logs_folder = os.path.join(settings.TEST_RESOURCES, 'activity_logs')
    basic_activity_log = os.path.join(activity_logs_folder, 'basic_activity.json')
    activity_log_file_path = os.path.join(activity_logs_folder, 'activity_upload_test.json')
    wrong_activity_file = os.path.join(activity_logs_folder, 'wrong_format.json')
    new_user_activity = os.path.join(activity_logs_folder, 'new_user_activity.json')
    quiz_attempt_log = os.path.join(activity_logs_folder, 'quiz_attempts.json')
    multiple_users = os.path.join(activity_logs_folder, 'multiple_users.json')

    url = '/api/activitylog/'
    username = 'demo'

    def setUp(self):
        super(ActivitylogUploadTest, self).setUp()
        user = User.objects.get(username=self.username)
        api_key = get_api_key(user=user)
        self.api_key = api_key.key

    def get_credentials(self):
        return self.create_apikey(username=self.username, api_key=self.api_key)


    def test_correct_data(self):

        initial_datacount = DataRecovery.objects.count()
        with open(self.basic_activity_log) as activity_log_file:
            json_data = json.load(activity_log_file)

        response = self.api_client.patch(self.url,
                                         format='json',
                                         data=json_data,
                                         authentication=self.get_credentials())
        self.assertEqual(200, response.status_code)
        self.assertEqual(initial_datacount, DataRecovery.objects.count() )


    def test_wrong_server(self):
        initial_datacount = DataRecovery.objects.count()
        with open(self.basic_activity_log) as activity_log_file:
            json_data = json.load(activity_log_file)

        json_data['server'] = 'another_server'

        self.api_client.patch(self.url,
                                         format='json',
                                         data=json_data,
                                         authentication=self.get_credentials())

        self.assertEqual(initial_datacount + 1, DataRecovery.objects.count())
        last_data = DataRecovery.objects.all().latest('pk')
        self.assertTrue(DataRecovery.Reason.DIFFERENT_TRACKER_SERVER in last_data.reasons)


    def test_wrong_format(self):
        initial_datacount = DataRecovery.objects.count()
        self.api_client.patch(self.url,
                              format='json',
                              data={'what':'some random data'},
                              authentication=self.get_credentials())

        self.assertEqual(initial_datacount + 1, DataRecovery.objects.count())
        last_data = DataRecovery.objects.all().latest('pk')
        self.assertTrue(DataRecovery.Reason.MISSING_SERVER in last_data.reasons)


    def test_trackers_missing(self):
        initial_datacount = DataRecovery.objects.count()
        with open(self.basic_activity_log) as activity_log_file:
            json_data = json.load(activity_log_file)

        for user in json_data['users']:
            del user['trackers']

        self.api_client.patch(self.url,
                              format='json',
                              data=json_data,
                              authentication=self.get_credentials())

        self.assertEqual(initial_datacount + 1, DataRecovery.objects.count())
        last_data = DataRecovery.objects.all().latest('pk')
        self.assertTrue(DataRecovery.Reason.MISSING_TRACKERS_TAG in last_data.reasons)


    def test_quizzes_missing(self):
        initial_datacount = DataRecovery.objects.count()
        with open(self.basic_activity_log) as activity_log_file:
            json_data = json.load(activity_log_file)

        for user in json_data['users']:
            del user['quizresponses']

        self.api_client.patch(self.url,
                              format='json',
                              data=json_data,
                              authentication=self.get_credentials())

        self.assertEqual(initial_datacount + 1, DataRecovery.objects.count())
        last_data = DataRecovery.objects.all().latest('pk')
        self.assertTrue(DataRecovery.Reason.MISSING_QUIZRESPONSES_TAG in last_data.reasons)


    def test_userprofile_missing_customfields(self):
        initial_datacount = DataRecovery.objects.count()
        with open(self.basic_activity_log) as activity_log_file:
            json_data = json.load(activity_log_file)

        for user in json_data['users']:
            user['missing_customfield'] = 'test'

        response = self.api_client.patch(self.url,
                                        format='json',
                                        data=json_data,
                                        authentication=self.get_credentials())

        self.assertEqual(initial_datacount + 1, DataRecovery.objects.count())
        last_data = DataRecovery.objects.all().latest('pk')
        self.assertTrue(DataRecovery.Reason.CUSTOM_PROFILE_FIELDS_NOT_DEFINED_IN_THE_SERVER in last_data.reasons)