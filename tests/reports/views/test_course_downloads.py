import datetime

from django.urls import reverse
from django.utils import timezone

from oppia.test import OppiaTestCase


class CourseDownloadsViewTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_cohort.json',
                'tests/test_course_permissions.json',
                'tests/test_usercoursesummary.json',
                'default_gamification_events.json',
                'tests/test_tracker.json']

    template = 'reports/course_downloads.html'
    url = reverse('reports:course_downloads')

    def setUp(self):
        super(CourseDownloadsViewTest, self).setUp()
        self.allowed_users = [self.admin_user, self.staff_user]
        self.disallowed_users = [self.teacher_user, self.normal_user]

    def test_course_downloads_get(self):
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

    def test_course_downloads_previous_date(self):
        self.client.force_login(self.admin_user)
        start_date = timezone.now() - datetime.timedelta(days=31)
        response = self.client.post(self.url,
                                    data={'start_date': start_date})
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

    def test_course_downloads_future_date(self):
        self.client.force_login(self.admin_user)
        start_date = timezone.now() + datetime.timedelta(days=31)
        response = self.client.post(self.url,
                                    data={'start_date': start_date})
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

    def test_course_downloads_invalid_date(self):
        self.client.force_login(self.admin_user)
        start_date = "not a valid date"
        response = self.client.post(self.url,
                                    data={'start_date': start_date})
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(200, response.status_code)
