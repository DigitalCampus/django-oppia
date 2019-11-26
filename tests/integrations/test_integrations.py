# tests/integrations/test_integrations.py
from django.urls import reverse
from django.test import TestCase

from tests.user_logins import ADMIN_USER, \
                              STAFF_USER, \
                              NORMAL_USER, \
                              TEACHER_USER


class IntegrationViewsTest(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']

    def setUp(self):
        super(IntegrationViewsTest, self).setUp()
        self.login_url = reverse('profile_login')

    def get_view(self, route, user=None):
        if user is not None:
            self.client.login(username=user['user'],
                              password=user['password'])
        return self.client.get(route)

    def test_anon_cantview_integrations_home(self):
        route = reverse('oppia_integrations_home')
        res = self.get_view(route, None)
        self.assertRedirects(res, self.login_url + '?next=/integrations/')

    def test_admin_canview_integrations_home(self):
        route = reverse('oppia_integrations_home')
        res = self.get_view(route, ADMIN_USER)
        self.assertEqual(res.status_code, 200)

    def test_staff_canview_integrations_home(self):
        route = reverse('oppia_integrations_home')
        res = self.get_view(route, STAFF_USER)
        self.assertEqual(res.status_code, 200)

    def test_student_cantview_integrations_home(self):
        route = reverse('oppia_integrations_home')
        res = self.get_view(route, NORMAL_USER)
        self.assertRedirects(res, '/admin/login/?next=/integrations/')

    def test_user_with_canupload_integrations_home(self):
        route = reverse('oppia_integrations_home')
        res = self.get_view(route, TEACHER_USER)
        self.assertRedirects(res, '/admin/login/?next=/integrations/')
