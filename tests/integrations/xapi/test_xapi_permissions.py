# tests/integrations/dhis/test_dhis.py
from django.urls import reverse
from django.test import TestCase

from tests.user_logins import ADMIN_USER, \
                              STAFF_USER, \
                              NORMAL_USER, \
                              TEACHER_USER


class XAPIIntegrationViewsTest(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']

    def setUp(self):
        super(XAPIIntegrationViewsTest, self).setUp()
        self.login_url = reverse('profile_login')

    def get_view(self, route, user=None):
        if user is not None:
            self.client.login(username=user['user'],
                              password=user['password'])
        return self.client.get(route)

    # test permissions for home

    def test_anon_cantview_integrations_home(self):
        route = reverse('oppia_integrations_xapi_home')
        res = self.get_view(route, None)
        self.assertRedirects(res,
                             self.login_url + '?next=/integrations/xapi/')

    def test_admin_canview_integrations_home(self):
        route = reverse('oppia_integrations_xapi_home')
        res = self.get_view(route, ADMIN_USER)
        self.assertEqual(res.status_code, 200)

    def test_staff_canview_integrations_home(self):
        route = reverse('oppia_integrations_xapi_home')
        res = self.get_view(route, STAFF_USER)
        self.assertEqual(res.status_code, 200)

    def test_student_cantview_integrations_home(self):
        route = reverse('oppia_integrations_xapi_home')
        res = self.get_view(route, NORMAL_USER)
        self.assertRedirects(res, '/admin/login/?next=/integrations/xapi/')

    def test_user_with_canupload_integrations_home(self):
        route = reverse('oppia_integrations_xapi_home')
        res = self.get_view(route, TEACHER_USER)
        self.assertRedirects(res, '/admin/login/?next=/integrations/xapi/')

    # test permissions and response for latest

    def test_anon_cantview_integrations_latest(self):
        route = reverse('oppia_integrations_xapi_csv_export')
        res = self.get_view(route, None)
        self.assertRedirects(
            res,
            self.login_url + '?next=/integrations/xapi/export/')

    def test_admin_canview_integrations_latest(self):
        route = reverse('oppia_integrations_xapi_csv_export')
        res = self.get_view(route, ADMIN_USER)
        self.assertEqual(res.status_code, 200)

    def test_staff_canview_integrations_latest(self):
        route = reverse('oppia_integrations_xapi_csv_export')
        res = self.get_view(route, STAFF_USER)
        self.assertEqual(res.status_code, 200)

    def test_student_cantview_integrations_latest(self):
        route = reverse('oppia_integrations_xapi_csv_export')
        res = self.get_view(route, NORMAL_USER)
        self.assertRedirects(res,
                             '/admin/login/?next=/integrations/xapi/export/')

    def test_user_with_canupload_integrations_latest(self):
        route = reverse('oppia_integrations_xapi_csv_export')
        res = self.get_view(route, TEACHER_USER)
        self.assertRedirects(res,
                             '/admin/login/?next=/integrations/xapi/export/')
