
from django.urls import reverse
from oppia.test import OppiaTestCase


class DownloadTimeTrackingViewTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_cohort.json',
                'tests/test_course_permissions.json',
                'tests/test_usercoursesummary.json',
                'tests/test_customfields.json']

    url = reverse('reports:user-course-time-spent')

    STR_EXPECTED_CONTENT_TYPE = 'application/text;charset=utf-8'

    def setUp(self):
        super(DownloadTimeTrackingViewTest, self).setUp()
        self.allowed_users = [self.admin_user, self.staff_user]
        self.disallowed_users = [self.teacher_user, self.normal_user]

    def test_permissions(self):

        for allowed_user in self.allowed_users:
            self.client.force_login(user=allowed_user)
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['content-type'],
                             self.STR_EXPECTED_CONTENT_TYPE)
            self.assertEqual('attachment; filename=time_tracking.csv',
                             response['Content-Disposition'])

        for disallowed_user in self.disallowed_users:
            self.client.force_login(user=disallowed_user)
            response = self.client.get(self.url)
            self.assertRedirects(response,
                                 '/admin/login/?next=' + self.url,
                                 302,
                                 200)
