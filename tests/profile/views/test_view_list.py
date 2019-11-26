from django.urls import reverse
from django.test import TestCase

from tests.user_logins import ADMIN_USER, \
                              STAFF_USER, \
                              NORMAL_USER, \
                              TEACHER_USER


class UserSearchActivityViewTest(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']

    def setUp(self):
        super(UserSearchActivityViewTest, self).setUp()
        self.template = 'profile/users-paginated-list.html'
        self.url = reverse('profile_list_users')

    def test_view_export(self):

        allowed_users = [ADMIN_USER, STAFF_USER]
        disallowed_users = [TEACHER_USER, NORMAL_USER]

        for allowed_user in allowed_users:
            self.client.login(username=allowed_user['user'],
                              password=allowed_user['password'])
            response = self.client.get(self.url)
            self.assertTemplateUsed(response, self.template)
            self.assertEqual(response.status_code, 200)

        for disallowed_user in disallowed_users:
            self.client.login(username=disallowed_user['user'],
                              password=disallowed_user['password'])
            response = self.client.get(self.url)
            self.assertRedirects(response,
                                 '/admin/login/?next=' + self.url,
                                 302,
                                 200)
