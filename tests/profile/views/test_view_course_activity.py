from django.urls import reverse
from oppia.test import OppiaTestCase

from tests.defaults import UNAUTHORISED_TEMPLATE


class CourseActivityViewTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']

    def setUp(self):
        super(CourseActivityViewTest, self).setUp()
        self.template = 'profile/user-course-scorecard.html'
        self.course_id = 1
        self.reverse_url = 'profile:user_course_activity'

    def test_view_own_course_activity(self):

        allowed_users = [self.admin_user,
                         self.staff_user,
                         self.teacher_user,
                         self.normal_user]

        for allowed_user in allowed_users:
            url = reverse(self.reverse_url, args=[allowed_user.id,
                                                  self.course_id])
            self.client.force_login(user=allowed_user)
            response = self.client.get(url)
            self.assertTemplateUsed(response, self.template)
            self.assertEqual(response.status_code, 200)

    def test_admin_view_others_course_activity(self):

        url = reverse(self.reverse_url, args=[self.staff_user.id,
                                              self.course_id])
        self.client.force_login(user=self.admin_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

        url = reverse(self.reverse_url, args=[self.teacher_user.id,
                                              self.course_id])
        self.client.force_login(user=self.admin_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

        url = reverse(self.reverse_url, args=[self.normal_user.id,
                                              self.course_id])
        self.client.force_login(user=self.admin_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

    def test_staff_view_others_course_activity(self):

        url = reverse(self.reverse_url, args=[self.admin_user.id,
                                              self.course_id])
        self.client.force_login(user=self.staff_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

        url = reverse(self.reverse_url, args=[self.teacher_user.id,
                                              self.course_id])
        self.client.force_login(user=self.staff_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

        url = reverse(self.reverse_url, args=[self.normal_user.id,
                                              self.course_id])
        self.client.force_login(user=self.staff_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

    def test_teacher_view_others_course_activity(self):

        url = reverse(self.reverse_url, args=[self.admin_user.id,
                                              self.course_id])
        self.client.force_login(user=self.teacher_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)
        self.assertEqual(response.status_code, 403)

        url = reverse(self.reverse_url, args=[self.staff_user.id,
                                              self.course_id])
        self.client.force_login(user=self.teacher_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)
        self.assertEqual(response.status_code, 403)

        url = reverse(self.reverse_url, args=[self.normal_user.id,
                                              self.course_id])
        self.client.force_login(user=self.teacher_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)
        self.assertEqual(response.status_code, 403)

    def test_user_view_others_course_activity(self):

        url = reverse(self.reverse_url, args=[self.admin_user.id,
                                              self.course_id])
        self.client.force_login(user=self.normal_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)
        self.assertEqual(response.status_code, 403)

        url = reverse(self.reverse_url, args=[self.staff_user.id,
                                              self.course_id])
        self.client.force_login(user=self.normal_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)
        self.assertEqual(response.status_code, 403)

        url = reverse(self.reverse_url, args=[self.teacher_user.id,
                                              self.course_id])
        self.client.force_login(user=self.normal_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)
        self.assertEqual(response.status_code, 403)
