
from django.urls import reverse
from oppia.test import OppiaTestCase


class TotalTimeSpentViewTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_cohort.json',
                'tests/test_course_permissions.json',
                'tests/test_usercoursesummary.json',
                'tests/test_customfields.json',
                'tests/test_daus.json']

    url = reverse('reports:totaltimespent')
    template = 'reports/total_time_spent.html'

    def setUp(self):
        super(TotalTimeSpentViewTest, self).setUp()
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
            
    def test_total_time_custom_dates(self):
        self.client.force_login(self.admin_user)
        start_date = "2015-01-01"
        end_date = "2019-12-31"
        response = self.client.post(self.url,
                                    data={'start_date': start_date,
                                          'end_date': end_date})
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)
