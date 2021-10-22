
from django.contrib.auth.models import User
from django.test import TransactionTestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url


class DownloadDataResourceTest(ResourceTestCaseMixin, TransactionTestCase):
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
    STR_EXPECTED_CONTENT_TYPE = 'text/html'

    def setUp(self):
        super(DownloadDataResourceTest, self).setUp()
        self.user = User.objects.get(username='demo')
        self.admin = User.objects.get(username='admin')
        self.staff = User.objects.get(username='staff')
        self.teacher = User.objects.get(username='teacher')
        self.user_auth = {
            'username': 'demo',
            'api_key': get_api_key(user=self.user).key,
        }
        self.admin_auth = {
            'username': 'admin',
            'api_key': get_api_key(user=self.admin).key
        }
        self.staff_auth = {
            'username': 'staff',
            'api_key': get_api_key(user=self.staff).key
        }
        self.teacher_auth = {
            'username': 'teacher',
            'api_key': get_api_key(user=self.teacher).key
        }
        self.url = get_api_url('v2', 'downloaddata')

    def test_post_not_allowed(self):
        self.assertHttpMethodNotAllowed(
            self.api_client.post(self.url, format='json', data={}))

    def test_list_not_allowed(self):
        resp = self.api_client.get(
            self.url, format='json', data=self.user_auth)
        self.assertHttpBadRequest(resp)

    def test_individual_not_allowed(self):
        resp = self.api_client.get(
            self.url + "2/", format='json', data=self.user_auth)
        self.assertHttpBadRequest(resp)

    def test_get_activity_user(self):
        resp = self.api_client.get(
            self.url + self.STR_ACTIVITY, format='json', data=self.user_auth)
        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="demo-activity.html"',
                         resp['Content-Disposition'])

    def test_get_activity_admin(self):
        resp = self.api_client.get(
            self.url + self.STR_ACTIVITY, format='json', data=self.admin_auth)
        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="admin-activity.html"',
                         resp['Content-Disposition'])

    def test_get_activity_staff(self):
        resp = self.api_client.get(
            self.url + self.STR_ACTIVITY, format='json', data=self.staff_auth)
        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="staff-activity.html"',
                         resp['Content-Disposition'])

    def test_get_activity_teacher(self):
        resp = self.api_client.get(
            self.url + self.STR_ACTIVITY,
            format='json',
            data=self.teacher_auth)
        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="teacher-activity.html"',
                         resp['Content-Disposition'])

    def test_get_quiz_user(self):
        resp = self.api_client.get(
            self.url + self.STR_QUIZ, format='json', data=self.user_auth)
        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="demo-quizzes.html"',
                         resp['Content-Disposition'])

    def test_get_quiz_admin(self):
        resp = self.api_client.get(
            self.url + self.STR_QUIZ, format='json', data=self.admin_auth)
        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="admin-quizzes.html"',
                         resp['Content-Disposition'])

    def test_get_quiz_staff(self):
        resp = self.api_client.get(
            self.url + self.STR_QUIZ, format='json', data=self.staff_auth)
        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="staff-quizzes.html"',
                         resp['Content-Disposition'])

    def test_get_quiz_teacher(self):
        resp = self.api_client.get(
            self.url + self.STR_QUIZ, format='json', data=self.teacher_auth)
        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="teacher-quizzes.html"',
                         resp['Content-Disposition'])

    def test_get_badges_user(self):
        resp = self.api_client.get(
            self.url + self.STR_BADGES, format='json', data=self.user_auth)
        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="demo-badges.html"',
                         resp['Content-Disposition'])

    def test_get_badges_admin(self):
        resp = self.api_client.get(
            self.url + self.STR_BADGES, format='json', data=self.admin_auth)
        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="admin-badges.html"',
                         resp['Content-Disposition'])

    def test_get_badges_staff(self):
        resp = self.api_client.get(
            self.url + self.STR_BADGES, format='json', data=self.staff_auth)
        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="staff-badges.html"',
                         resp['Content-Disposition'])

    def test_get_badges_teacher(self):
        resp = self.api_client.get(
            self.url + self.STR_BADGES, format='json', data=self.teacher_auth)
        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="teacher-badges.html"',
                         resp['Content-Disposition'])

    def test_get_points_user(self):
        resp = self.api_client.get(
            self.url + self.STR_POINTS, format='json', data=self.user_auth)
        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="demo-points.html"',
                         resp['Content-Disposition'])

    def test_get_points_admin(self):
        resp = self.api_client.get(
            self.url + self.STR_POINTS, format='json', data=self.admin_auth)
        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="admin-points.html"',
                         resp['Content-Disposition'])

    def test_get_points_staff(self):
        resp = self.api_client.get(
            self.url + self.STR_POINTS, format='json', data=self.staff_auth)
        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="staff-points.html"',
                         resp['Content-Disposition'])

    def test_get_points_teacher(self):
        resp = self.api_client.get(
            self.url + self.STR_POINTS, format='json', data=self.teacher_auth)

        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="teacher-points.html"',
                         resp['Content-Disposition'])

    def test_get_profile_user(self):
        resp = self.api_client.get(
            self.url + self.STR_PROFILE, format='json', data=self.user_auth)
        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="demo-profile.html"',
                         resp['Content-Disposition'])

    def test_get_profile_admin(self):
        resp = self.api_client.get(
            self.url + self.STR_PROFILE, format='json', data=self.admin_auth)
        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="admin-profile.html"',
                         resp['Content-Disposition'])

    def test_get_profile_staff(self):
        resp = self.api_client.get(
            self.url + self.STR_PROFILE, format='json', data=self.staff_auth)
        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="staff-profile.html"',
                         resp['Content-Disposition'])

    def test_get_profile_teacher(self):
        resp = self.api_client.get(
            self.url + self.STR_PROFILE, format='json', data=self.teacher_auth)
        self.assertHttpOK(resp)
        self.assertEqual(resp['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        self.assertEqual('attachment; filename="teacher-profile.html"',
                         resp['Content-Disposition'])
