
from django.urls import reverse
from oppia.test import OppiaTestCase


class LoginViewTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_cohort.json',
                'tests/test_course_permissions.json']

    def test_already_logged_in_admin(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(self.login_url)
        self.assertRedirects(response, reverse('oppia:index'), 302, 200)

    def test_already_logged_in_staff(self):
        self.client.force_login(user=self.staff_user)
        response = self.client.get(self.login_url)
        self.assertRedirects(response, reverse('oppia:index'), 302, 200)

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

    def test_login_no_redirect(self):
        data = {'username': 'admin',
                'password': 'password'}
        response = self.client.post(self.login_url, data=data)
        self.assertRedirects(response, reverse('oppia:index'), 302, 200)

    def test_login_valid_redirect(self):
        data = {'username': 'admin',
                'password': 'password',
                'next': '/course/'}
        response = self.client.post(self.login_url, data=data)
        self.assertRedirects(response, reverse('oppia:course'), 302, 200)

    def test_login_invalid_redirect(self):
        data = {'username': 'admin',
                'password': 'password',
                'next': 'http://mysite.com/'}
        response = self.client.post(self.login_url, data=data)
        self.assertRedirects(response, reverse('oppia:index'), 302, 200)

    def test_teacher_login_redirect(self):
        data = {'username': 'teacher',
                'password': 'password'}
        response = self.client.post(self.login_url, data=data)
        # should redirect twice - to index then to teacher view
        self.assertRedirects(response, reverse('oppia:index'), 302, 302)

    def test_manager_login_redirect(self):
        data = {'username': 'manager',
                'password': 'manager'}
        response = self.client.post(self.login_url, data=data)
        # should redirect twice - to index then to manager view
        self.assertRedirects(response, reverse('oppia:index'), 302, 302)
