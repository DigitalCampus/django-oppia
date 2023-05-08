import unittest
import pytest

from rest_framework.test import APITestCase

from tests.api.v3 import utils


class DownloadUserDataTests(APITestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_permissions.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'tests/test_quiz.json',
                'tests/test_quizattempt.json']

    STR_ACTIVITY = 'activity/'
    STR_QUIZ = 'quiz/'
    STR_BADGES = 'badges/'
    STR_POINTS = 'points/'
    STR_PROFILE = 'profile/'
    STR_FEEDBACK = 'profile/'
    STR_EXPECTED_CONTENT_TYPE = 'text/html'

    url = "/api/v3/userdata/"

    def make_get_request(self, user_auth, data_type):
        url = self.url + data_type
        return self.client.get(url, headers=user_auth)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_post_not_allowed(self):
        response = self.client.post(self.url, headers=utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_METHOD_NOT_ALLOWED)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_list_not_allowed(self):
        response = self.client.get(self.url, headers=utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_METHOD_NOT_ALLOWED)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_individual_not_allowed(self):
        response = self.client.get(self.url + "2/", headers=utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_METHOD_NOT_ALLOWED)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_activity_user(self):
        response = self.make_get_request(utils.get_auth_header_user(), self.STR_ACTIVITY)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="demo-activity.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_activity_admin(self):
        response = self.make_get_request(utils.get_auth_header_admin(), self.STR_ACTIVITY)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="admin-activity.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_activity_staff(self):
        response = self.make_get_request(utils.get_auth_header_staff(), self.STR_ACTIVITY)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="staff-activity.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_activity_teacher(self):
        response = self.make_get_request(utils.get_auth_header_teacher(), self.STR_ACTIVITY)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="teacher-activity.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_quiz_user(self):
        response = self.make_get_request(utils.get_auth_header_user(), self.STR_QUIZ)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="demo-quizzes.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_quiz_admin(self):
        response = self.make_get_request(utils.get_auth_header_admin(), self.STR_QUIZ)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="admin-quizzes.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_quiz_staff(self):
        response = self.make_get_request(utils.get_auth_header_staff(), self.STR_QUIZ)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="staff-quizzes.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_quiz_teacher(self):
        response = self.make_get_request(utils.get_auth_header_teacher(), self.STR_QUIZ)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="teacher-quizzes.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_badges_user(self):
        response = self.make_get_request(utils.get_auth_header_user(), self.STR_BADGES)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="demo-badges.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_badges_admin(self):
        response = self.make_get_request(utils.get_auth_header_admin(), self.STR_BADGES)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="admin-badges.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_badges_staff(self):
        response = self.make_get_request(utils.get_auth_header_staff(), self.STR_BADGES)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="staff-badges.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_badges_teacher(self):
        response = self.make_get_request(utils.get_auth_header_teacher(), self.STR_BADGES)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="teacher-badges.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_points_user(self):
        response = self.make_get_request(utils.get_auth_header_user(), self.STR_POINTS)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="demo-points.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_points_admin(self):
        response = self.make_get_request(utils.get_auth_header_admin(), self.STR_POINTS)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="admin-points.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_points_staff(self):
        response = self.make_get_request(utils.get_auth_header_staff(), self.STR_POINTS)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="staff-points.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_points_teacher(self):
        response = self.make_get_request(utils.get_auth_header_teacher(), self.STR_POINTS)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="teacher-points.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_profile_user(self):
        response = self.make_get_request(utils.get_auth_header_user(), self.STR_PROFILE)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="demo-profile.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_profile_admin(self):
        response = self.make_get_request(utils.get_auth_header_admin(), self.STR_PROFILE)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="admin-profile.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_profile_staff(self):
        response = self.make_get_request(utils.get_auth_header_staff(), self.STR_PROFILE)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="staff-profile.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_profile_teacher(self):
        response = self.make_get_request(utils.get_auth_header_teacher(), self.STR_PROFILE)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="teacher-profile.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_feedback_user(self):
        response = self.make_get_request(utils.get_auth_header_user(), self.STR_FEEDBACK)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="demo-feedback.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_feedback_admin(self):
        response = self.make_get_request(utils.get_auth_header_admin(), self.STR_FEEDBACK)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="admin-feedback.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_feedback_staff(self):
        response = self.make_get_request(utils.get_auth_header_staff(), self.STR_FEEDBACK)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="staff-feedback.html"', response.get('Content-Disposition'))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_feedback_teacher(self):
        response = self.make_get_request(utils.get_auth_header_teacher(), self.STR_FEEDBACK)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="teacher-feedback.html"', response.get('Content-Disposition'))
