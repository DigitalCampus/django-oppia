from oppia.test import OppiaTestCase

from django.contrib.auth.models import User
from django.urls import reverse

from oppia.models import Tracker
from quiz.models import QuizAttemptResponse, QuizAttempt


class UploadActivityLogTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_malaria_quiz.json',
                'tests/test_permissions.json',
                'default_gamification_events.json',
                'tests/test_course_permissions.json']

    url = reverse('activitylog:upload')
    basic_activity_log = './oppia/fixtures/activity_logs/basic_activity.json'
    activity_log_file_path = \
        './oppia/fixtures/activity_logs/activity_upload_test.json'
    wrong_activity_file = './oppia/fixtures/activity_logs/wrong_format.json'
    new_user_activity = './oppia/fixtures/activity_logs/new_user_activity.json'
    quiz_attempt_log = './oppia/fixtures/activity_logs/quiz_attempts.json'

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
        self.assertRedirects(response,
                             reverse('activitylog:upload_success'),
                             302,
                             200)

        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start + 2, tracker_count_end)

    def test_new_user_file(self):
        tracker_count_start = Tracker.objects.all().count()
        user_count_start = User.objects.all().count()

        self.client.force_login(self.admin_user)

        with open(self.new_user_activity, 'rb') as activity_log_file:
            response = self.client.post(self.url,
                                        {'activity_log_file':
                                         activity_log_file})

        # should be redirected to the update step 2 form
        self.assertRedirects(response,
                             reverse('activitylog:upload_success'),
                             302,
                             200)

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

        self.assertRedirects(response,
                             reverse('activitylog:upload_success'),
                             302,
                             200)

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

        self.assertRedirects(response,
                             reverse('activitylog:upload_success'),
                             302,
                             200)

        # Now upload the same file
        with open(self.basic_activity_log, 'rb') as activity_log_file:
            response = self.client.post(self.url,
                                        {'activity_log_file':
                                         activity_log_file})

        self.assertRedirects(response,
                             reverse('activitylog:upload_success'),
                             302,
                             200)

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

        self.assertRedirects(response,
                             reverse('activitylog:upload_success'),
                             302,
                             200)

        # Now upload the same file
        with open(self.quiz_attempt_log, 'rb') as activity_log_quiz_file:
            response = self.client.post(self.url,
                                        {'activity_log_file':
                                         activity_log_quiz_file})

        self.assertRedirects(response,
                             reverse('activitylog:upload_success'),
                             302,
                             200)

        tracker_count_end = Tracker.objects.all().count()
        qa_count_end = QuizAttempt.objects.all().count()
        qar_count_end = QuizAttemptResponse.objects.all().count()

        self.assertEqual(tracker_count_start, tracker_count_end)
        self.assertEqual(qa_count_start + 1, qa_count_end)
        self.assertEqual(qar_count_start + 7, qar_count_end)
