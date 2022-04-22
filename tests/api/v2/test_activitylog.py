import json
import os

from django.contrib.auth.models import User
from django.test import TestCase
from django.conf import settings

from activitylog.models import UploadedActivityLog
from oppia.models import Tracker
from quiz.models import QuizAttemptResponse, QuizAttempt
from tastypie.test import ResourceTestCaseMixin
from tests.utils import get_api_key


class UploadAPIActivityLogTest(ResourceTestCaseMixin, TestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_malaria_quiz.json',
                'tests/test_settings.json',
                'tests/test_permissions.json',
                'default_gamification_events.json']

    url = '/api/activitylog/'
    activity_logs_folder = os.path.join(settings.TEST_RESOURCES, 'activity_logs')
    basic_activity_log = os.path.join(activity_logs_folder, 'basic_activity.json')
    activity_log_file_path = os.path.join(activity_logs_folder, 'activity_upload_test.json')
    wrong_activity_file = os.path.join(activity_logs_folder, 'wrong_format.json')
    new_user_activity = os.path.join(activity_logs_folder, 'new_user_activity.json')
    quiz_attempt_log = os.path.join(activity_logs_folder, 'quiz_attempts.json')
    multiple_users = os.path.join(activity_logs_folder, 'multiple_users.json')

    def setUp(self):
        super(UploadAPIActivityLogTest, self).setUp()
        self.username = 'demo'
        user = User.objects.get(username=self.username)
        api_key = get_api_key(user=user)
        self.api_key = api_key.key

    def get_credentials(self):
        return self.create_apikey(username=self.username,
                                  api_key=self.api_key)

    def test_no_get(self):
        response = self.api_client.get(self.url)
        self.assertEqual(405, response.status_code)

    def test_no_post(self):
        response = self.api_client.post(self.url,
                                        format='json',
                                        data={})
        self.assertEqual(405, response.status_code)

    def test_no_data(self):
        # no file
        response = self.api_client.patch(self.url,
                                         format='json',
                                         data={},
                                         authentication=self.get_credentials())
        self.assertEqual(400, response.status_code)

    def test_correct_basic_data(self):
        uploaded_count_start = UploadedActivityLog.objects.all().count()
        tracker_count_start = Tracker.objects.all().count()

        with open(self.basic_activity_log) as activity_log_file:
            json_data = json.load(activity_log_file)

        response = self.api_client.patch(self.url,
                                         format='json',
                                         data=json_data,
                                         authentication=self.get_credentials())
        self.assertEqual(200, response.status_code)

        tracker_count_end = Tracker.objects.all().count()
        uploaded_count_end = UploadedActivityLog.objects.all().count()
        last_uploaded = UploadedActivityLog.objects.all() \
            .order_by('-created_date').first()
        self.assertEqual(tracker_count_start + 2, tracker_count_end)
        self.assertEqual(uploaded_count_start + 1, uploaded_count_end)
        self.assertEqual(last_uploaded.create_user.username, 'demo')
        self.assertIn('demo', last_uploaded.file.name)

    def test_new_user_file(self):
        tracker_count_start = Tracker.objects.all().count()
        user_count_start = User.objects.all().count()
        uploaded_count_start = UploadedActivityLog.objects.all().count()
        with open(self.new_user_activity) as activity_log_file:
            json_data = json.load(activity_log_file)

        response = self.api_client.patch(self.url,
                                         format='json',
                                         data=json_data,
                                         authentication=self.get_credentials())

        self.assertEqual(200, response.status_code)
        tracker_count_end = Tracker.objects.all().count()
        user_count_end = User.objects.all().count()
        uploaded_count_end = UploadedActivityLog.objects.all().count()
        last_uploaded = UploadedActivityLog.objects.all() \
            .order_by('-created_date').first()

        self.assertEqual(tracker_count_start + 2, tracker_count_end)
        self.assertEqual(user_count_start + 1, user_count_end)
        self.assertEqual(uploaded_count_start + 1, uploaded_count_end)
        self.assertEqual(last_uploaded.create_user.username, 'newuser')
        self.assertIn('newuser', last_uploaded.file.name)

    def test_multiple_users_data(self):
        uploaded_count_start = UploadedActivityLog.objects.all().count()
        tracker_count_start = Tracker.objects.all().count()

        with open(self.multiple_users) as activity_log_file:
            json_data = json.load(activity_log_file)

        response = self.api_client.patch(self.url,
                                         format='json',
                                         data=json_data,
                                         authentication=self.get_credentials())
        self.assertEqual(200, response.status_code)

        tracker_count_end = Tracker.objects.all().count()
        uploaded_count_end = UploadedActivityLog.objects.all().count()
        last_uploaded = UploadedActivityLog.objects.all() \
            .order_by('-created_date').first()
        self.assertEqual(tracker_count_start + 4, tracker_count_end)
        self.assertEqual(uploaded_count_start + 1, uploaded_count_end)
        self.assertEqual(last_uploaded.create_user.username, 'demo')
        self.assertIn('activity', last_uploaded.file.name)

    def test_wrong_format_file(self):

        with open(self.wrong_activity_file) as activity_log_file:
            json_data = json.load(activity_log_file)

        response = self.api_client.patch(self.url,
                                         format='json',
                                         data=json_data,
                                         authentication=self.get_credentials())

        self.assertEqual(400, response.status_code)

    def test_quizattempts(self):
        tracker_count_start = Tracker.objects.all().count()
        qa_count_start = QuizAttempt.objects.all().count()
        qar_count_start = QuizAttemptResponse.objects.all().count()

        with open(self.quiz_attempt_log) as activity_log_file:
            json_data = json.load(activity_log_file)

        response = self.api_client.patch(self.url,
                                         format='json',
                                         data=json_data,
                                         authentication=self.get_credentials())

        self.assertEqual(200, response.status_code)
        tracker_count_end = Tracker.objects.all().count()
        qa_count_end = QuizAttempt.objects.all().count()
        qar_count_end = QuizAttemptResponse.objects.all().count()

        self.assertEqual(tracker_count_start, tracker_count_end)
        self.assertEqual(qa_count_start + 1, qa_count_end)
        self.assertEqual(qar_count_start + 7, qar_count_end)

    def test_trackers_not_duplicated(self):
        tracker_count_start = Tracker.objects.all().count()

        with open(self.basic_activity_log) as activity_log_file:
            json_data = json.load(activity_log_file)

        response = self.api_client.patch(self.url,
                                         format='json',
                                         data=json_data,
                                         authentication=self.get_credentials())
        self.assertEqual(200, response.status_code)

        # Now upload the same file
        with open(self.basic_activity_log) as activity_log_file:
            json_data = json.load(activity_log_file)

        response = self.api_client.patch(self.url,
                                         format='json',
                                         data=json_data,
                                         authentication=self.get_credentials())

        self.assertEqual(200, response.status_code)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start + 2, tracker_count_end)

    def test_quizattempts_not_duplicated(self):
        tracker_count_start = Tracker.objects.all().count()
        qa_count_start = QuizAttempt.objects.all().count()
        qar_count_start = QuizAttemptResponse.objects.all().count()

        with open(self.quiz_attempt_log) as activity_log_file:
            json_data = json.load(activity_log_file)

        response = self.api_client.patch(self.url,
                                         format='json',
                                         data=json_data,
                                         authentication=self.get_credentials())

        self.assertEqual(200, response.status_code)

        # Now upload the same file
        with open(self.quiz_attempt_log) as activity_log_file:
            json_data = json.load(activity_log_file)

        response = self.api_client.patch(self.url,
                                         format='json',
                                         data=json_data,
                                         authentication=self.get_credentials())

        self.assertEqual(200, response.status_code)

        tracker_count_end = Tracker.objects.all().count()
        qa_count_end = QuizAttempt.objects.all().count()
        qar_count_end = QuizAttemptResponse.objects.all().count()

        self.assertEqual(tracker_count_start, tracker_count_end)
        self.assertEqual(qa_count_start + 1, qa_count_end)
        self.assertEqual(qar_count_start + 7, qar_count_end)
