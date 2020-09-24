
from django.urls import reverse
from oppia.test import OppiaTestCase


class GamificationPermissionsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_course_permissions.json']
    valid_course_url = reverse('oppia_gamification_edit_course', args=[1])
    invalid_course_url = reverse('oppia_gamification_edit_course', args=[55])

    def testCoursePointsEdit(self):
        # admin
        self.client.force_login(self.admin_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 200)

        # staff
        self.client.force_login(self.staff_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 200)

        # teacher
        self.client.force_login(self.teacher_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)

        # user
        self.client.force_login(self.normal_user)
        response = self.client.get(self.valid_course_url)
        self.assertEqual(response.status_code, 403)

    def testUnknownCoursePointsEdit(self):

        # admin
        self.client.force_login(self.admin_user)
        response = self.client.get(self.invalid_course_url)
        self.assertEqual(response.status_code, 404)

        # staff
        self.client.force_login(self.staff_user)
        response = self.client.get(self.invalid_course_url)
        self.assertEqual(response.status_code, 404)

        # teacher
        self.client.force_login(self.teacher_user)
        response = self.client.get(self.invalid_course_url)
        self.assertEqual(response.status_code, 403)

        # user
        self.client.force_login(self.normal_user)
        response = self.client.get(self.invalid_course_url)
        self.assertEqual(response.status_code, 403)
