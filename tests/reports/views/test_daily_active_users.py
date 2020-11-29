
from django.urls import reverse
from oppia.test import OppiaTestCase


class DailyActiveUsersViewTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_cohort.json',
                'tests/test_course_permissions.json',
                'tests/test_usercoursesummary.json',
                'tests/test_customfields.json',
                'tests/test_daus.json']

    url = reverse('reports:daus')
    template = 'reports/daus.html'

    def setUp(self):
        super(DailyActiveUsersViewTest, self).setUp()
        self.allowed_users = [self.admin_user, self.staff_user]
        self.disallowed_users = [self.teacher_user, self.normal_user]

    def test_permissions(self):

        for allowed_user in self.allowed_users:
            self.client.force_login(user=allowed_user)
            response = self.client.get(self.url)
            self.assertTemplateUsed(response, self.template)
            self.assertEqual(response.status_code, 200)

        for disallowed_user in self.disallowed_users:
            self.client.force_login(user=disallowed_user)
            response = self.client.get(self.url)
            self.assertRedirects(response,
                                 '/admin/login/?next=' + self.url,
                                 302,
                                 200)
            
    def test_old_dates(self):
        self.client.force_login(user=self.admin_user)
        data = {'start_date': "2000-01-01",
                'end_date': "2000-12-31"}
        response = self.client.post(self.url, data=data)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)
        
