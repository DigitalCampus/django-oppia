from django.contrib.auth.models import User
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
        self.admin_user = User.objects.get(pk=ADMIN_USER['id'])
        self.staff_user = User.objects.get(pk=STAFF_USER['id'])
        self.teacher_user = User.objects.get(pk=TEACHER_USER['id'])
        self.normal_user = User.objects.get(pk=NORMAL_USER['id'])

    def test_home_view(self):
        url = reverse('oppia_av_home')
        allowed_users = [self.admin_user,
                         self.staff_user,
                         self.staff_user,
                         self.normal_user]

        for allowed_user in allowed_users:
            self.client.force_login(allowed_user)
            response = self.client.get(url)
            self.assertTemplateUsed(response, 'av/home.html')
            self.assertEqual(response.status_code, 200)
