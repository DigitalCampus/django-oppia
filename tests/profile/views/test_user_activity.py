from django.urls import reverse
from django.test import TestCase

from tests.user_logins import ADMIN_USER, \
                              STAFF_USER, \
                              NORMAL_USER, \
                              TEACHER_USER


class UserActivityViewTest(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']

    def setUp(self):
        super(UserActivityViewTest, self).setUp()
        self.template = 'profile/user-scorecard.html'
        self.unauthorised_template = '403.html'

    def test_view_own_activity(self):

        allowed_users = [ADMIN_USER, STAFF_USER, TEACHER_USER, NORMAL_USER]

        for allowed_user in allowed_users:
            url = reverse('profile_user_activity', args=[allowed_user['id']])
            self.client.login(username=allowed_user['user'],
                              password=allowed_user['password'])
            response = self.client.get(url)
            self.assertTemplateUsed(response, self.template)
            self.assertEqual(response.status_code, 200)

    def test_admin_view_others_activity(self):
        url = reverse('profile_user_activity', args=[STAFF_USER['id']])
        self.client.login(username=ADMIN_USER['user'],
                          password=ADMIN_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

        url = reverse('profile_user_activity', args=[TEACHER_USER['id']])
        self.client.login(username=ADMIN_USER['user'],
                          password=ADMIN_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

        url = reverse('profile_user_activity', args=[NORMAL_USER['id']])
        self.client.login(username=ADMIN_USER['user'],
                          password=ADMIN_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

    def test_staff_view_others_activity(self):
        url = reverse('profile_user_activity', args=[ADMIN_USER['id']])
        self.client.login(username=STAFF_USER['user'],
                          password=STAFF_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

        url = reverse('profile_user_activity', args=[TEACHER_USER['id']])
        self.client.login(username=STAFF_USER['user'],
                          password=STAFF_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

        url = reverse('profile_user_activity', args=[NORMAL_USER['id']])
        self.client.login(username=STAFF_USER['user'],
                          password=STAFF_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

    def test_teacher_view_others_activity(self):
        url = reverse('profile_user_activity', args=[ADMIN_USER['id']])
        self.client.login(username=TEACHER_USER['user'],
                          password=TEACHER_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, '403.html')
        self.assertEqual(response.status_code, 403)

        url = reverse('profile_user_activity', args=[STAFF_USER['id']])
        self.client.login(username=TEACHER_USER['user'],
                          password=TEACHER_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.unauthorised_template)
        self.assertEqual(response.status_code, 403)

        url = reverse('profile_user_activity', args=[NORMAL_USER['id']])
        self.client.login(username=TEACHER_USER['user'],
                          password=TEACHER_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.unauthorised_template)
        self.assertEqual(response.status_code, 403)

    def test_user_view_others_activity(self):
        url = reverse('profile_user_activity', args=[ADMIN_USER['id']])
        self.client.login(username=NORMAL_USER['user'],
                          password=NORMAL_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.unauthorised_template)
        self.assertEqual(response.status_code, 403)

        url = reverse('profile_user_activity', args=[STAFF_USER['id']])
        self.client.login(username=NORMAL_USER['user'],
                          password=NORMAL_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.unauthorised_template)
        self.assertEqual(response.status_code, 403)

        url = reverse('profile_user_activity', args=[TEACHER_USER['id']])
        self.client.login(username=NORMAL_USER['user'],
                          password=NORMAL_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.unauthorised_template)
        self.assertEqual(response.status_code, 403)
