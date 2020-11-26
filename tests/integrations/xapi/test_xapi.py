import datetime

from django.urls import reverse
from django.utils import timezone

from oppia.models import Tracker
from oppia.test import OppiaTestCase


class XAPIIntegrationViewsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_gamification_events.json',
                'tests/test_course_permissions.json',
                'tests/test_tracker.json',
                'tests/test_quizattempt.json']

    def setUp(self):
        super(XAPIIntegrationViewsTest, self).setUp()
        self.xapi_home_url = reverse('integrations:xapi:index')
        self.xapi_export_url = reverse('integrations:xapi:export')

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

    # test download file
    def test_admin_canview_download_file(self):
        four_days_ago = timezone.now() - datetime.timedelta(days=4)
        for tracker in Tracker.objects.all():
            tracker.tracker_date = four_days_ago
            tracker.submitted_date = four_days_ago
            tracker.save()
        response = self.get_view(self.xapi_export_url, self.admin_user)
        self.assertEqual(response.status_code, 200)
