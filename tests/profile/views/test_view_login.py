
from django.urls import reverse
from oppia.test import OppiaTestCase


class LoginViewTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_cohort.json']

    def test_already_logged_in_admin(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(self.login_url)
        self.assertRedirects(response, reverse('oppia_home'), 302, 200)

    def test_already_logged_in_staff(self):
        self.client.force_login(user=self.staff_user)
        response = self.client.get(self.login_url)
        self.assertRedirects(response, reverse('oppia_home'), 302, 200)

    def test_already_logged_in_teacher(self):
        self.client.force_login(user=self.teacher_user)
        response = self.client.get(self.login_url, follow=True)
        self.assertTemplateUsed(response, 'oppia/home-teacher.html')
        self.assertEqual(response.status_code, 200)

    def test_already_logged_in_user(self):
        self.client.force_login(user=self.normal_user)
        response = self.client.get(self.login_url, follow=True)
        self.assertTemplateUsed(response, 'profile/user-scorecard.html')
        self.assertEqual(response.status_code, 200)
