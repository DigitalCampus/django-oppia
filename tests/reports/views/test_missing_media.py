from django.urls import reverse
from oppia.test import OppiaTestCase
from oppia.models import Tracker


class MissingMediaViewTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_permissions.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'tests/test_course_permissions.json',
                'tests/test_missing_media_trackers.json']

    report_url = reverse('reports:missing_media')
    report_template = 'reports/missing_media.html'

    purge_form_url = reverse('reports:missing_media_purge', args=[3])
    purge_form_template = 'reports/missing_media_confirm_purge.html'
    purge_complete_template = 'reports/missing_media_purged.html'

    def setUp(self):
        super(MissingMediaViewTest, self).setUp()
        self.allowed_users = [self.admin_user, self.staff_user]
        self.disallowed_users = [self.teacher_user, self.normal_user]

    def test_permissions(self):

        for allowed_user in self.allowed_users:
            self.client.force_login(user=allowed_user)
            response = self.client.get(self.report_url)
            self.assertTemplateUsed(response, self.report_template)
            self.assertEqual(response.status_code, 200)

        for disallowed_user in self.disallowed_users:
            self.client.force_login(user=disallowed_user)
            response = self.client.get(self.report_url)
            self.assertRedirects(response,
                                 '/admin/login/?next=' + self.report_url,
                                 302,
                                 200)
            response = self.client.get(self.purge_form_url)
            self.assertRedirects(response,
                                 '/admin/login/?next=' + self.purge_form_url,
                                 302,
                                 200)
            response = self.client.post(self.purge_form_url)
            self.assertRedirects(response,
                                 '/admin/login/?next=' + self.purge_form_url,
                                 302,
                                 200)

    def test_purge_get_form(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(self.purge_form_url)
        self.assertTemplateUsed(response, self.purge_form_template)
        self.assertEqual(response.status_code, 200)

    def test_purge_post_form(self):
        self.client.force_login(user=self.admin_user)
        count_start = Tracker.objects.all().count()
        response = self.client.post(self.purge_form_url)
        self.assertTemplateUsed(response, self.purge_complete_template)
        self.assertEqual(response.status_code, 200)

        count_end = Tracker.objects.all().count()
        self.assertEqual(count_start-2, count_end)
