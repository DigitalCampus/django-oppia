import io
import tablib

from django.urls import reverse

from oppia.test import OppiaTestCase

from tests.defaults import UNAUTHORISED_TEMPLATE


class FeedbackDownloadTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_feedback.json',
                'default_gamification_events.json',
                'tests/test_course_permissions.json']
    STR_EXPECTED_CONTENT_TYPE = 'application/vnd.ms-excel;charset=utf-8'
    STR_URL_TEMPLATE = 'quiz:feedback_results_download'
    STR_URL_OLD_FEEDBACK_TEMPLATE = 'quiz:old_feedback_results_download'

    valid_course_valid_feedback_url = reverse(STR_URL_TEMPLATE, args=[183, 65323])
    invalid_course_valid_feedback_url = reverse(STR_URL_TEMPLATE, args=[0, 65323])
    valid_course_invalid_feedback_url = reverse(STR_URL_TEMPLATE, args=[183, 0])
    invalid_course_invalid_feedback_url = reverse(STR_URL_TEMPLATE, args=[0, 0])
    course_feedback_mismatch_url = reverse(STR_URL_TEMPLATE, args=[1, 65323])

    def test_admin_download(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.valid_course_valid_feedback_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.STR_EXPECTED_CONTENT_TYPE, response['content-type'])
        downloaded_file = io.BytesIO(response.content)
        dataset = tablib.import_set(downloaded_file)
        self.assertEqual(dataset.headers[0], "Date")
        self.assertEqual(dataset.headers[1], "UserId")
        self.assertEqual(dataset.headers[2], "Username")
        self.assertEqual(len(dataset.headers), 19)

    def test_staff_download(self):
        response = self.assert_response_status(self.staff_user, self.valid_course_valid_feedback_url, 200)
        self.assertEqual(self.STR_EXPECTED_CONTENT_TYPE, response['content-type'])
        downloaded_file = io.BytesIO(response.content)
        dataset = tablib.import_set(downloaded_file)
        self.assertEqual(dataset.headers[0], "Date")
        self.assertEqual(dataset.headers[1], "UserId")
        self.assertEqual(dataset.headers[2], "Username")
        self.assertEqual(len(dataset.headers), 19)

    def test_teacher_download(self):
        response = self.assert_response_status(self.teacher_user, self.valid_course_valid_feedback_url, 403)
        self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)

    def test_user_download(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(self.valid_course_valid_feedback_url)
        self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)
        self.assertEqual(403, response.status_code)

    def test_invalid_course_valid_feedback(self):
        users = [self.admin_user,
                 self.staff_user,
                 self.teacher_user,
                 self.normal_user]
        for user in users:
            self.assert_response_status(user, self.invalid_course_valid_feedback_url, 404)

    def test_valid_course_invalid_feedback(self):
        for user in [self.admin_user, self.staff_user]:
            self.assert_response_status(user, self.valid_course_invalid_feedback_url, 404)
        for user in [self.teacher_user, self.normal_user]:
            self.assert_response_status(user, self.valid_course_invalid_feedback_url, 403)

    def test_invalid_course_invalid_feedback(self):
        users = [self.admin_user,
                 self.staff_user,
                 self.teacher_user,
                 self.normal_user]
        for user in users:
            self.assert_response_status(user, self.invalid_course_invalid_feedback_url, 404)

    def test_course_feedback_mismatch(self):

        for user in [self.admin_user, self.staff_user]:
            self.assert_response_status(user, self.course_feedback_mismatch_url, 404)
        for user in [self.teacher_user, self.normal_user]:
            self.assert_response_status(user, self.course_feedback_mismatch_url, 403)

    def test_old_feedback_download(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse(self.STR_URL_OLD_FEEDBACK_TEMPLATE, args=[183, 24]))
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.STR_EXPECTED_CONTENT_TYPE, response['content-type'])
        downloaded_file = io.BytesIO(response.content)
        dataset = tablib.import_set(downloaded_file)
        self.assertEqual(dataset.headers[0], "Date")
        self.assertEqual(dataset.headers[1], "UserId")
        self.assertEqual(dataset.headers[2], "Username")
        self.assertEqual(len(dataset.headers), 19)
