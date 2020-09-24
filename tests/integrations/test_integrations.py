from django.urls import reverse
from oppia.test import OppiaTestCase


class IntegrationViewsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']

    def setUp(self):
        super(IntegrationViewsTest, self).setUp()
        self.intgrations_home_url = reverse('integrations:index')

    def test_anon_cantview_integrations_home(self):
        res = self.get_view(self.intgrations_home_url, None)
        self.assertRedirects(res, self.login_url + '?next=/integrations/')

    def test_admin_canview_integrations_home(self):
        res = self.get_view(self.intgrations_home_url, self.admin_user)
        self.assertEqual(res.status_code, 200)

    def test_staff_canview_integrations_home(self):
        res = self.get_view(self.intgrations_home_url, self.staff_user)
        self.assertEqual(res.status_code, 200)

    def test_student_cantview_integrations_home(self):
        res = self.get_view(self.intgrations_home_url, self.normal_user)
        self.assertRedirects(res, '/admin/login/?next=/integrations/')

    def test_user_with_canupload_integrations_home(self):
        res = self.get_view(self.intgrations_home_url, self.teacher_user)
        self.assertRedirects(res, '/admin/login/?next=/integrations/')
