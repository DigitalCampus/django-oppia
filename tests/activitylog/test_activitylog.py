import os

from oppia.test import OppiaTestCase

from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

from oppia.models import Tracker
from profile.models import UserProfile, UserProfileCustomField, CustomField
from quiz.models import QuizAttemptResponse, QuizAttempt


class UploadActivityLogTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_customfields.json',
                'tests/test_oppia.json',
                'tests/test_malaria_quiz.json',
                'tests/test_settings.json',
                'tests/test_permissions.json',
                'default_gamification_events.json',
                'tests/test_course_permissions.json']

    url = reverse('activitylog:upload')

    activity_logs_folder = os.path.join(settings.TEST_RESOURCES, 'activity_logs')
    basic_activity_log = os.path.join(activity_logs_folder, 'basic_activity.json')
    activity_log_file_path = os.path.join(activity_logs_folder, 'activity_upload_test.json')
    wrong_activity_file = os.path.join(activity_logs_folder, 'wrong_format.json')
    new_user_activity = os.path.join(activity_logs_folder, 'new_user_activity.json')
    quiz_attempt_log = os.path.join(activity_logs_folder, 'quiz_attempts.json')
    file_with_emojis = os.path.join(activity_logs_folder, 'file_with_emojis.json')
    activity_with_emojis = os.path.join(activity_logs_folder, 'activity_emojis.json')
    activity_with_userinfo = os.path.join(activity_logs_folder, 'activity_with_userinfo.json')
    activity_with_empty_userinfo = os.path.join(activity_logs_folder, 'activity_with_empty_userinfo.json')
    activity_with_nulled_userinfo = os.path.join(activity_logs_folder, 'activity_with_nulled_userinfo.json')

    def assert_redirects_success(self, response):
        self.assertRedirects(response,
                             reverse('activitylog:upload_success'), 302, 200)

    def test_no_file(self):
        # no file
        self.client.force_login(self.admin_user)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response,
                             'form',
                             'activity_log_file',
                             'Please select an activity log file to upload')

    def test_wrong_format_file(self):
        self.client.force_login(self.admin_user)
        with open(self.wrong_activity_file, 'rb') as activity_log_file:
            response = self.client.post(self.url,
                                        {'activity_log_file':
                                         activity_log_file})

        messages = list(response.context['messages'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(messages), 1)
        self.assertContains(response, 'wrong format')

    def test_correct_file(self):
        tracker_count_start = Tracker.objects.all().count()

        self.client.force_login(self.admin_user)

        with open(self.basic_activity_log, 'rb') as activity_log_file:
            response = self.client.post(self.url,
                                        {'activity_log_file':
                                         activity_log_file})

        # should be redirected to the success page
        self.assert_redirects_success(response)

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start + 2, tracker_count_end)

    def test_userprofile_updated(self):

        self.client.force_login(self.admin_user)

        with open(self.activity_with_userinfo, 'rb') as activity_log_file:
            response = self.client.post(self.url,
                                        {'activity_log_file':
                                         activity_log_file})

        # should be redirected to the success page
        self.assert_redirects_success(response)

        user = User.objects.get(username='demo')
        userprofile = UserProfile.objects.get(user=user)
        self.assertEqual(userprofile.phone_number, '123456789')
        self.assertEqual(userprofile.organisation, 'home')
        self.assertEqual(UserProfileCustomField.get_user_value(
            user, 'country'), 'ES')
        self.assertEqual(UserProfileCustomField.get_user_value(
            user, 'agree_to_terms'), True)

    def test_empty_userprofile_doesnt_update_fields(self):

        user = User.objects.get(username='demo')
        userprofile = UserProfile.objects.get(user=user)
        userprofile.phone_number = '123456789'
        userprofile.organisation = 'home'
        userprofile.save()

        self.client.force_login(self.admin_user)

        with open(self.basic_activity_log, 'rb') as activity_log_file:
            response = self.client.post(self.url,
                                        {'activity_log_file':
                                         activity_log_file})

        # should be redirected to the success page
        self.assert_redirects_success(response)

        userprofile = UserProfile.objects.get(user=user)
        self.assertEqual(userprofile.phone_number, '123456789')
        self.assertEqual(userprofile.organisation, 'home')
        self.assertEqual(UserProfileCustomField.get_user_value(
            user, 'country'), 'FI')
        self.assertEqual(UserProfileCustomField.get_user_value(
            user, 'agree_to_terms'), None)

    def test_empty_string_userprofile_doesnt_update_fields(self):

        user = User.objects.get(username='demo')
        userprofile = UserProfile.objects.get(user=user)
        userprofile.phone_number = '123456789'
        userprofile.organisation = 'home'
        userprofile.save()

        self.client.force_login(self.admin_user)

        with open(self.activity_with_empty_userinfo, 'rb') as alf:
            response = self.client.post(self.url,
                                        {'activity_log_file': alf})

        # should be redirected to the success page
        self.assert_redirects_success(response)

        userprofile = UserProfile.objects.get(user=user)
        self.assertEqual(userprofile.phone_number, '123456789')
        self.assertEqual(userprofile.organisation, 'home')
        self.assertEqual(UserProfileCustomField.get_user_value(
            user, 'country'), 'FI')

    def test_null_string_userprofile_doesnt_update_fields(self):

        user = User.objects.get(username='demo')
        userprofile = UserProfile.objects.get(user=user)
        userprofile.phone_number = '123456789'
        userprofile.organisation = 'home'
        userprofile.save()

        self.client.force_login(self.admin_user)

        with open(self.activity_with_nulled_userinfo, 'rb') as alf:
            response = self.client.post(self.url,
                                        {'activity_log_file': alf})

        # should be redirected to the success page
        self.assert_redirects_success(response)

        userprofile = UserProfile.objects.get(user=user)
        self.assertEqual(userprofile.phone_number, '123456789')
        self.assertEqual(userprofile.organisation, 'home')
        self.assertEqual(UserProfileCustomField.get_user_value(
            user, 'country'), 'FI')

    def test_empty_string_userprofile_creates_nonexistent_custom_fields(self):
        # If a user profile is submitted that contains empty string custom
        # fields that didn't exist previously, in that case those fields should
        # be created with the empty value

        user = User.objects.get(username='demo')
        # remove user custom fields

        CustomField.objects.create(
            id='extra',
            type='str',
            required=True,
            label='Required'
        )

        UserProfileCustomField.objects.filter(user=user).delete()
        self.assertEqual(UserProfileCustomField.get_user_value(
            user, 'country'), None)
        self.assertEqual(UserProfileCustomField.get_user_value(
            user, 'extra'), None)
        self.client.force_login(self.admin_user)

        with open(self.activity_with_empty_userinfo, 'rb') as alf:
            response = self.client.post(self.url,
                                        {'activity_log_file': alf})

        # should be redirected to the success page
        self.assert_redirects_success(response)
        # "extra" field is required, so the CustomField is created anyway
        self.assertEqual(UserProfileCustomField.get_user_value(
            user, 'extra'), '')
        # Country field is not required, so is not created with an empty value
        self.assertEqual(UserProfileCustomField.get_user_value(
            user, 'country'), None)

    def test_file_with_emojis(self):
        tracker_count_start = Tracker.objects.all().count()
        user_count_start = User.objects.all().count()

        self.client.force_login(self.admin_user)

        with open(self.activity_with_emojis, 'rb') as activity_log_file:
            response = self.client.post(self.url,
                                        {'activity_log_file':
                                         activity_log_file})

        # should be redirected to the update step 2 form
        self.assert_redirects_success(response)
        user_count_end = User.objects.all().count()
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start + 1, tracker_count_end)
        self.assertEqual(user_count_start, user_count_end)

    def test_new_user_file(self):
        tracker_count_start = Tracker.objects.all().count()
        user_count_start = User.objects.all().count()

        self.client.force_login(self.admin_user)

        with open(self.new_user_activity, 'rb') as activity_log_file:
            response = self.client.post(self.url,
                                        {'activity_log_file':
                                         activity_log_file})

        # should be redirected to the update step 2 form
        self.assert_redirects_success(response)

        tracker_count_end = Tracker.objects.all().count()
        user_count_end = User.objects.all().count()
        self.assertEqual(tracker_count_start + 2, tracker_count_end)
        self.assertEqual(user_count_start + 1, user_count_end)

    def test_quizattempts(self):
        tracker_count_start = Tracker.objects.all().count()
        qa_count_start = QuizAttempt.objects.all().count()
        qar_count_start = QuizAttemptResponse.objects.all().count()

        self.client.force_login(self.admin_user)

        with open(self.quiz_attempt_log, 'rb') as activity_log_quiz_file:
            response = self.client.post(self.url,
                                        {'activity_log_file':
                                         activity_log_quiz_file})

        self.assert_redirects_success(response)

        tracker_count_end = Tracker.objects.all().count()
        qa_count_end = QuizAttempt.objects.all().count()
        qar_count_end = QuizAttemptResponse.objects.all().count()

        self.assertEqual(tracker_count_start, tracker_count_end)
        self.assertEqual(qa_count_start + 1, qa_count_end)
        self.assertEqual(qar_count_start + 7, qar_count_end)

    def test_trackers_not_duplicated(self):
        tracker_count_start = Tracker.objects.all().count()

        self.client.force_login(self.admin_user)

        with open(self.basic_activity_log, 'rb') as activity_log_file:
            response = self.client.post(self.url,
                                        {'activity_log_file':
                                         activity_log_file})

        self.assert_redirects_success(response)

        # Now upload the same file
        with open(self.basic_activity_log, 'rb') as activity_log_file:
            response = self.client.post(self.url,
                                        {'activity_log_file':
                                         activity_log_file})

        self.assert_redirects_success(response)

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start + 2, tracker_count_end)

    def test_quizattempts_not_duplicated(self):
        tracker_count_start = Tracker.objects.all().count()
        qa_count_start = QuizAttempt.objects.all().count()
        qar_count_start = QuizAttemptResponse.objects.all().count()

        self.client.force_login(self.admin_user)

        with open(self.quiz_attempt_log, 'rb') as activity_log_quiz_file:
            response = self.client.post(self.url,
                                        {'activity_log_file':
                                         activity_log_quiz_file})

        self.assert_redirects_success(response)

        # Now upload the same file
        with open(self.quiz_attempt_log, 'rb') as activity_log_quiz_file:
            response = self.client.post(self.url,
                                        {'activity_log_file':
                                         activity_log_quiz_file})

        self.assert_redirects_success(response)

        tracker_count_end = Tracker.objects.all().count()
        qa_count_end = QuizAttempt.objects.all().count()
        qar_count_end = QuizAttemptResponse.objects.all().count()

        self.assertEqual(tracker_count_start, tracker_count_end)
        self.assertEqual(qa_count_start + 1, qa_count_end)
        self.assertEqual(qar_count_start + 7, qar_count_end)

    def test_file_with_emojis2(self):
        tracker_count_start = Tracker.objects.all().count()

        self.client.force_login(self.admin_user)

        with open(self.file_with_emojis, 'rb') as activity_log_file:
            response = self.client.post(self.url,
                                        {'activity_log_file':
                                         activity_log_file})

        # should be redirected to the success page
        self.assertRedirects(response,
                             reverse('activitylog:upload_success'),
                             302,
                             200)

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+2, tracker_count_end)
