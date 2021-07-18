from django.urls import reverse
from oppia.test import OppiaTestCase


class AVPagesViewTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json',
                'tests/test_cohort.json',
                'tests/test_av_uploadedmedia.json']

    index_url = reverse('av:index')
    index_template = 'av/home.html'

    def test_home_view(self):
        allowed_users = [self.admin_user,
                         self.staff_user,
                         self.teacher_user,
                         self.normal_user]

        for allowed_user in allowed_users:
            self.client.force_login(allowed_user)
            response = self.client.get(self.index_url)
            self.assertTemplateUsed(response, self.index_template)
            self.assertEqual(response.status_code, 200)

    def test_home_view_invalid_page_param(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(self.index_url + "?page=abc")
        self.assertTemplateUsed(response, self.index_template)
        self.assertEqual(response.status_code, 200)

    def test_home_view_invalid_page_no(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(self.index_url + "?page=999")
        self.assertTemplateUsed(response, self.index_template)
        self.assertEqual(response.status_code, 200)
