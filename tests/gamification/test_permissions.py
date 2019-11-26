
from django.urls import reverse
from django.test import TestCase

from tests.user_logins import ADMIN_USER, \
                              STAFF_USER, \
                              NORMAL_USER, \
                              TEACHER_USER


class GamificationPermissionsTest(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json']

    def setUp(self):
        super(GamificationPermissionsTest, self).setUp()

    def testCoursePointsEdit(self):
        # admin
        self.client.login(username=ADMIN_USER['user'],
                          password=ADMIN_USER['password'])
        response = self.client.get(reverse('oppia_gamification_edit_course',
                                           args=[1]))
        self.assertEqual(response.status_code, 200)

        # staff
        self.client.login(username=STAFF_USER['user'],
                          password=STAFF_USER['password'])
        response = self.client.get(reverse('oppia_gamification_edit_course',
                                           args=[1]))
        self.assertEqual(response.status_code, 200)

        # teacher
        self.client.login(username=TEACHER_USER['user'],
                          password=TEACHER_USER['password'])
        response = self.client.get(reverse('oppia_gamification_edit_course',
                                           args=[1]))
        self.assertEqual(response.status_code, 403)

        # user
        self.client.login(username=NORMAL_USER['user'],
                          password=NORMAL_USER['password'])
        response = self.client.get(reverse('oppia_gamification_edit_course',
                                           args=[1]))
        self.assertEqual(response.status_code, 403)

    def testUnknownCoursePointsEdit(self):

        # admin
        self.client.login(username=ADMIN_USER['user'],
                          password=ADMIN_USER['password'])
        response = self.client.get(reverse('oppia_gamification_edit_course',
                                           args=[55]))
        self.assertEqual(response.status_code, 404)

        # staff
        self.client.login(username=STAFF_USER['user'],
                          password=STAFF_USER['password'])
        response = self.client.get(reverse('oppia_gamification_edit_course',
                                           args=[55]))
        self.assertEqual(response.status_code, 404)

        # teacher
        self.client.login(username=TEACHER_USER['user'],
                          password=TEACHER_USER['password'])
        response = self.client.get(reverse('oppia_gamification_edit_course',
                                           args=[55]))
        self.assertEqual(response.status_code, 403)

        # user
        self.client.login(username=NORMAL_USER['user'],
                          password=NORMAL_USER['password'])
        response = self.client.get(reverse('oppia_gamification_edit_course',
                                           args=[55]))
        self.assertEqual(response.status_code, 403)
