
from django.urls import reverse
from oppia.test import OppiaTestCase


class ManagerCourseViewsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']

    def test_home_view_redirect(self):
        self.client.force_login(user=self.manager_user)
        url = reverse('oppia:index')
        response = self.client.get(url)
        self.assertRedirects(response,
                             reverse('oppia:manager_index'),
                             302,
                             200)

    def test_manager_view_manager(self):
        self.client.force_login(user=self.manager_user)
        url = reverse('oppia:manager_index')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "oppia/home-manager.html")

    def test_manager_view_admin(self):
        self.client.force_login(user=self.admin_user)
        url = reverse('oppia:manager_index')
        response = self.client.get(url)
        self.assertEqual(403, response.status_code)
        self.assertTemplateUsed(self.unauthorized_template)

    def test_manager_view_staff(self):
        self.client.force_login(user=self.staff_user)
        url = reverse('oppia:manager_index')
        response = self.client.get(url)
        self.assertEqual(403, response.status_code)
        self.assertTemplateUsed(self.unauthorized_template)

    def test_manager_view_user(self):
        self.client.force_login(user=self.normal_user)
        url = reverse('oppia:manager_index')
        response = self.client.get(url)
        self.assertEqual(403, response.status_code)
        self.assertTemplateUsed(self.unauthorized_template)

    def test_manager_view_viewer(self):
        self.client.force_login(user=self.viewer_user)
        url = reverse('oppia:manager_index')
        response = self.client.get(url)
        self.assertEqual(403, response.status_code)
        self.assertTemplateUsed(self.unauthorized_template)

    def test_manager_view_teacher(self):
        self.client.force_login(user=self.teacher_user)
        url = reverse('oppia:manager_index')
        response = self.client.get(url)
        self.assertEqual(403, response.status_code)
        self.assertTemplateUsed(self.unauthorized_template)
