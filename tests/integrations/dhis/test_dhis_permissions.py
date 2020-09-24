from django.urls import reverse
from oppia.test import OppiaTestCase


class DHISIntegrationViewsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']

    def setUp(self):
        super(DHISIntegrationViewsTest, self).setUp()
        self.dhis_home_url = reverse('integrations:dhis:index')
        self.dhis_latest_url = reverse('integrations:dhis:export_latest')

    # test permissions for home

    def test_anon_cantview_integrations_home(self):
        response = self.client.get(self.dhis_home_url)
        self.assertRedirects(response,
                             self.login_url + '?next=/integrations/dhis/')

    def test_admin_canview_integrations_home(self):
        response = self.get_view(self.dhis_home_url, self.admin_user)
        self.assertEqual(response.status_code, 200)

    def test_staff_canview_integrations_home(self):
        response = self.get_view(self.dhis_home_url, self.staff_user)
        self.assertEqual(response.status_code, 200)

    def test_student_cantview_integrations_home(self):
        response = self.get_view(self.dhis_home_url, self.normal_user)
        self.assertRedirects(response,
                             '/admin/login/?next=/integrations/dhis/')

    def test_teacher_canupload_integrations_home(self):
        response = self.get_view(self.dhis_home_url, self.teacher_user)
        self.assertRedirects(response,
                             '/admin/login/?next=/integrations/dhis/')

    # test permissions and response for latest

    def test_anon_cantview_integrations_latest(self):
        response = self.client.get(self.dhis_latest_url)
        self.assertRedirects(response,
                             self.login_url
                             + '?next=/integrations/dhis/export/latest/')

    def test_admin_canview_integrations_latest(self):
        response = self.get_view(self.dhis_latest_url, self.admin_user)
        self.assertEqual(response.status_code, 200)

    def test_staff_canview_integrations_latest(self):
        response = self.get_view(self.dhis_latest_url, self.staff_user)
        self.assertEqual(response.status_code, 200)

    def test_student_cantview_integrations_latest(self):
        response = self.get_view(self.dhis_latest_url, self.normal_user)
        self.assertRedirects(
            response,
            '/admin/login/?next=/integrations/dhis/export/latest/')

    def test_user_with_canupload_integrations_latest(self):
        response = self.get_view(self.dhis_latest_url, self.teacher_user)
        self.assertRedirects(
            response,
            '/admin/login/?next=/integrations/dhis/export/latest/')

    # test permissions and response for other months

    def test_anon_cantview_integrations_monthly(self):
        route = reverse('integrations:dhis:export_month',
                        kwargs={'year': 2019, 'month': 10})
        res = self.get_view(route, None)
        self.assertRedirects(
            res,
            self.login_url + '?next=/integrations/dhis/export/2019/10')

    def test_admin_canview_integrations_monthly(self):
        route = reverse('integrations:dhis:export_month',
                        kwargs={'year': 2019, 'month': 10})
        res = self.get_view(route, self.admin_user)
        self.assertEqual(res.status_code, 200)

    def test_staff_canview_integrations_monthly(self):
        route = reverse('integrations:dhis:export_month',
                        kwargs={'year': 2019, 'month': 10})
        res = self.get_view(route, self.staff_user)
        self.assertEqual(res.status_code, 200)

    def test_student_cantview_integrations_monthly(self):
        route = reverse('integrations:dhis:export_month',
                        kwargs={'year': 2019, 'month': 10})
        res = self.get_view(route, self.normal_user)
        self.assertRedirects(
            res,
            '/admin/login/?next=/integrations/dhis/export/2019/10')

    def test_teacher_canupload_integrations_monthly(self):
        route = reverse('integrations:dhis:export_month',
                        kwargs={'year': 2019, 'month': 10})
        res = self.get_view(route, self.teacher_user)
        self.assertRedirects(
            res,
            '/admin/login/?next=/integrations/dhis/export/2019/10')
