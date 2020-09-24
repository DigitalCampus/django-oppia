from django.urls import reverse
from oppia.test import OppiaTestCase


class GamificationViewsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'default_gamification_events.json',
                'tests/test_course_permissions.json']

    export_server = reverse('oppia_gamification_leaderboard_export_server')
    STR_JSON_CONTENT_TYPE = "application/json"

    def test_leaderboard_export_admin(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.export_server)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.STR_JSON_CONTENT_TYPE, response['Content-Type'])

    def test_leaderboard_export_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(self.export_server)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.STR_JSON_CONTENT_TYPE, response['Content-Type'])

    def test_leaderboard_export_teacher(self):
        self.client.force_login(self.teacher_user)
        response = self.client.get(self.export_server)
        # will redirect to login
        self.assertEqual(response.status_code, 302)

    def test_leaderboard_export_normal(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(self.export_server)
        # will redirect to login
        self.assertEqual(response.status_code, 302)

    # for valid course
    def test_leaderboard_export_course_valid_admin(self):
        self.client.force_login(self.admin_user)
        url = reverse('oppia_gamification_leaderboard_export_course', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.STR_JSON_CONTENT_TYPE, response['Content-Type'])

    # for invalid course
    def test_leaderboard_export_course_invalid_admin(self):
        self.client.force_login(self.admin_user)
        url = reverse('oppia_gamification_leaderboard_export_course',
                      args=[121])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
