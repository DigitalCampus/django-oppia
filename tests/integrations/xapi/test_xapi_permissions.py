from django.urls import reverse
from oppia.test import OppiaTestCase


class XAPIIntegrationViewsTest(OppiaTestCase):

    def setUp(self):
        super(XAPIIntegrationViewsTest, self).setUp()
        self.xapi_home_url = reverse('oppia_integrations_xapi_home')
        self.xapi_export_url = reverse('oppia_integrations_xapi_csv_export')
        
    # test permissions for home

    def test_anon_cantview_integrations_home(self):
        response = self.client.get(self.xapi_home_url)
        self.assertRedirects(response,
                             self.login_url + '?next=/integrations/xapi/')

    def test_admin_canview_integrations_home(self):
        response = self.get_view(self.xapi_home_url, self.admin_user)
        self.assertEqual(response.status_code, 200)

    def test_staff_canview_integrations_home(self):
        response = self.get_view(self.xapi_home_url, self.staff_user)
        self.assertEqual(response.status_code, 200)

    def test_student_cantview_integrations_home(self):
        response = self.get_view(self.xapi_home_url, self.normal_user)
        self.assertRedirects(response,
                             '/admin/login/?next=/integrations/xapi/')

    def test_user_with_canupload_integrations_home(self):
        response = self.get_view(self.xapi_home_url, self.teacher_user)
        self.assertRedirects(response,
                             '/admin/login/?next=/integrations/xapi/')

    # test permissions and response for latest

    def test_anon_cantview_integrations_latest(self):
        response = self.get_view(self.xapi_export_url)
        self.assertRedirects(
            response,
            self.login_url + '?next=/integrations/xapi/export/')

    def test_admin_canview_integrations_latest(self):
        response = self.get_view(self.xapi_export_url, self.admin_user)
        self.assertEqual(response.status_code, 200)

    def test_staff_canview_integrations_latest(self):
        response = self.get_view(self.xapi_export_url, self.staff_user)
        self.assertEqual(response.status_code, 200)

    def test_student_cantview_integrations_latest(self):
        response = self.get_view(self.xapi_export_url, self.normal_user)
        self.assertRedirects(response,
                             '/admin/login/?next=/integrations/xapi/export/')

    def test_user_with_canupload_integrations_latest(self):
        response = self.get_view(self.xapi_export_url, self.teacher_user)
        self.assertRedirects(response,
                             '/admin/login/?next=/integrations/xapi/export/')
