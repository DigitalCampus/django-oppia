from django.core.paginator import InvalidPage
from django.urls import reverse
from oppia.test import OppiaTestCase


class PointsViewTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']

    url_points = reverse('profile:points')
    template = 'profile/points.html'

    def test_view_points(self):
        allowed_users = [self.admin_user,
                         self.staff_user,
                         self.teacher_user,
                         self.normal_user]

        for allowed_user in allowed_users:
            self.client.force_login(user=allowed_user)
            response = self.client.get(self.url_points)
            self.assertTemplateUsed(response, self.template)
            self.assertEqual(200, response.status_code)

    def test_points_page_1(self):
        self.client.force_login(user=self.admin_user)
        url = '%s?page=1' % self.url_points
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.template)

    def test_points_page_9999(self):
        self.client.force_login(user=self.admin_user)
        url = '%s?page=9999' % self.url_points
        response = self.client.get(url)
        self.assertRaises(InvalidPage)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.template)

    def test_points_page_def(self):
        self.client.force_login(user=self.admin_user)
        url = '%s?page=def' % self.url_points
        response = self.client.get(url)
        self.assertRaises(ValueError)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.template)
