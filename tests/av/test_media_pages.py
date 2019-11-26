from django.urls import reverse
from django.test import TestCase

from tests.user_logins import ADMIN_USER, \
                              STAFF_USER, \
                              NORMAL_USER, \
                              TEACHER_USER


class AVPagesViewTest(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']

    def setUp(self):
        super(AVPagesViewTest, self).setUp()

    def test_home_view(self):
        url = reverse('oppia_av_home')
        allowed_users = [ADMIN_USER, STAFF_USER, TEACHER_USER, NORMAL_USER]

        for allowed_user in allowed_users:
            self.client.login(username=allowed_user['user'],
                              password=allowed_user['password'])
            response = self.client.get(url)
            self.assertTemplateUsed(response, 'av/home.html')
            self.assertEqual(response.status_code, 200)
