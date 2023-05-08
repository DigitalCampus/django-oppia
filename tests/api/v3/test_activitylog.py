import unittest
import pytest
import os
import json

from django.conf import settings
from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from activitylog.models import UploadedActivityLog
from oppia.models import Tracker
from quiz.models import QuizAttemptResponse, QuizAttempt
from tests.api.v3 import utils


class ActivityLogAPITests(APITestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_malaria_quiz.json',
                'tests/test_settings.json',
                'tests/test_permissions.json',
                'default_gamification_events.json']

    url = '/api/v3/activitylog/'
    activity_logs_folder = os.path.join(settings.TEST_RESOURCES, 'activity_logs')
    basic_activity_log = os.path.join(activity_logs_folder, 'basic_activity.json')
    activity_log_file_path = os.path.join(activity_logs_folder, 'activity_upload_test.json')
    wrong_activity_file = os.path.join(activity_logs_folder, 'wrong_format.json')
    new_user_activity = os.path.join(activity_logs_folder, 'new_user_activity.json')
    quiz_attempt_log = os.path.join(activity_logs_folder, 'quiz_attempts.json')
    multiple_users = os.path.join(activity_logs_folder, 'multiple_users.json')

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_no_get(self):
        response = self.client.get(self.url, headers=utils.get_auth_header_user())
        self.assertEqual(utils.HTTP_METHOD_NOT_ALLOWED, response.status_code)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_no_post(self):
        response = self.client.post(self.url, data={}, headers=utils.get_auth_header_user())
        self.assertEqual(utils.HTTP_METHOD_NOT_ALLOWED, response.status_code)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_no_data(self):
        # no file
        response = self.client.patch(self.url, data={}, headers=utils.get_auth_header_user())
        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_correct_basic_data(self):
        uploaded_count_start = UploadedActivityLog.objects.all().count()
        tracker_count_start = Tracker.objects.all().count()

        with open(self.basic_activity_log) as activity_log_file:
            json_data = json.load(activity_log_file)

        response = self.client.patch(self.url, data=json_data, headers=utils.get_auth_header_user())
        self.assertEqual(utils.HTTP_OK, response.status_code)

        tracker_count_end = Tracker.objects.all().count()
        uploaded_count_end = UploadedActivityLog.objects.all().count()
        last_uploaded = UploadedActivityLog.objects.all().order_by('-created_date').first()
        self.assertEqual(tracker_count_start + 2, tracker_count_end)
        self.assertEqual(uploaded_count_start + 1, uploaded_count_end)
        self.assertEqual(last_uploaded.create_user.username, 'demo')
        self.assertIn('demo', last_uploaded.file.name)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_new_user_file(self):
        tracker_count_start = Tracker.objects.all().count()
        user_count_start = User.objects.all().count()
        uploaded_count_start = UploadedActivityLog.objects.all().count()
        with open(self.new_user_activity) as activity_log_file:
            json_data = json.load(activity_log_file)

        response = self.client.patch(self.url, data=json_data, headers=utils.get_auth_header_user())

        self.assertEqual(utils.HTTP_OK, response.status_code)
        tracker_count_end = Tracker.objects.all().count()
        user_count_end = User.objects.all().count()
        uploaded_count_end = UploadedActivityLog.objects.all().count()
        last_uploaded = UploadedActivityLog.objects.all().order_by('-created_date').first()

        self.assertEqual(tracker_count_start + 2, tracker_count_end)
        self.assertEqual(user_count_start + 1, user_count_end)
        self.assertEqual(uploaded_count_start + 1, uploaded_count_end)
        self.assertEqual(last_uploaded.create_user.username, 'newuser')
        self.assertIn('newuser', last_uploaded.file.name)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_multiple_users_data(self):
        uploaded_count_start = UploadedActivityLog.objects.all().count()
        tracker_count_start = Tracker.objects.all().count()

        with open(self.multiple_users) as activity_log_file:
            json_data = json.load(activity_log_file)

        response = self.client.patch(self.url, data=json_data, headers=utils.get_auth_header_user())
        self.assertEqual(utils.HTTP_OK, response.status_code)

        tracker_count_end = Tracker.objects.all().count()
        uploaded_count_end = UploadedActivityLog.objects.all().count()
        last_uploaded = UploadedActivityLog.objects.all().order_by('-created_date').first()
        self.assertEqual(tracker_count_start + 4, tracker_count_end)
        self.assertEqual(uploaded_count_start + 1, uploaded_count_end)
        self.assertEqual(last_uploaded.create_user.username, 'demo')
        self.assertIn('activity', last_uploaded.file.name)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_wrong_format_file(self):

        with open(self.wrong_activity_file) as activity_log_file:
            json_data = json.load(activity_log_file)

        response = self.client.patch(self.url, data=json_data, headers=utils.get_auth_header_user())

        self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_quizattempts(self):
        tracker_count_start = Tracker.objects.all().count()
        qa_count_start = QuizAttempt.objects.all().count()
        qar_count_start = QuizAttemptResponse.objects.all().count()

        with open(self.quiz_attempt_log) as activity_log_file:
            json_data = json.load(activity_log_file)

        response = self.client.patch(self.url, data=json_data, headers=utils.get_auth_header_user())

        self.assertEqual(utils.HTTP_OK, response.status_code)
        tracker_count_end = Tracker.objects.all().count()
        qa_count_end = QuizAttempt.objects.all().count()
        qar_count_end = QuizAttemptResponse.objects.all().count()

        self.assertEqual(tracker_count_start, tracker_count_end)
        self.assertEqual(qa_count_start + 1, qa_count_end)
        self.assertEqual(qar_count_start + 7, qar_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_trackers_not_duplicated(self):
        tracker_count_start = Tracker.objects.all().count()

        with open(self.basic_activity_log) as activity_log_file:
            json_data = json.load(activity_log_file)

        response = self.client.patch(self.url, data=json_data, headers=utils.get_auth_header_user())
        self.assertEqual(utils.HTTP_OK, response.status_code)

        # Now upload the same file
        with open(self.basic_activity_log) as activity_log_file:
            json_data = json.load(activity_log_file)

        response = self.client.patch(self.url, data=json_data, headers=utils.get_auth_header_user())

        self.assertEqual(utils.HTTP_OK, response.status_code)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start + 2, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_quizattempts_not_duplicated(self):
        tracker_count_start = Tracker.objects.all().count()
        qa_count_start = QuizAttempt.objects.all().count()
        qar_count_start = QuizAttemptResponse.objects.all().count()

        with open(self.quiz_attempt_log) as activity_log_file:
            json_data = json.load(activity_log_file)

        response = self.client.patch(self.url, data=json_data, headers=utils.get_auth_header_user())

        self.assertEqual(utils.HTTP_OK, response.status_code)

        # Now upload the same file
        with open(self.quiz_attempt_log) as activity_log_file:
            json_data = json.load(activity_log_file)

        response = self.client.patch(self.url, data=json_data, headers=utils.get_auth_header_user())

        self.assertEqual(utils.HTTP_OK, response.status_code)

        tracker_count_end = Tracker.objects.all().count()
        qa_count_end = QuizAttempt.objects.all().count()
        qar_count_end = QuizAttemptResponse.objects.all().count()

        self.assertEqual(tracker_count_start, tracker_count_end)
        self.assertEqual(qa_count_start + 1, qa_count_end)
        self.assertEqual(qar_count_start + 7, qar_count_end)
