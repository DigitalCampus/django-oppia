
from django.urls import reverse
from oppia.test import OppiaTestCase


class CourseCompletionRatesViewTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_course_statuses.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_cohort.json',
                'tests/test_course_permissions.json',
                'tests/test_usercoursesummary.json']

    def setUp(self):
        super(CourseCompletionRatesViewTest, self).setUp()
        self.allowed_users = [self.admin_user, self.staff_user]
        self.disallowed_users = [self.teacher_user, self.normal_user]

    def test_view_course_completion_rates_valid_course(self):
        url = reverse('reports:course_completion_rates', args=[1])
        template = 'reports/course_completion_rates.html'

        for allowed_user in self.allowed_users:
            self.client.force_login(user=allowed_user)
            response = self.client.get(url)
            self.assertTemplateUsed(response, template)
            self.assertEqual(response.status_code, 200)

        for disallowed_user in self.disallowed_users:
            self.client.force_login(user=disallowed_user)
            response = self.client.get(url)
            self.assertRedirects(response,
                                 '/admin/login/?next=' + url,
                                 302,
                                 200)

    def test_view_course_completion_rates_another_course(self):
        url = reverse('reports:course_completion_rates', args=[2])
        template = 'reports/course_completion_rates.html'
        self.client.force_login(user=self.admin_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, template)
        self.assertEqual(response.status_code, 200)

    def test_view_course_completion_rates_invalid_course(self):
        url = reverse('reports:course_completion_rates', args=[999])

        for allowed_user in self.allowed_users:
            self.client.force_login(user=allowed_user)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)

        for disallowed_user in self.disallowed_users:
            self.client.force_login(user=disallowed_user)
            response = self.client.get(url)
            self.assertRedirects(response,
                                 '/admin/login/?next=' + url,
                                 302,
                                 200)
