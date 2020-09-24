from django.urls import reverse
from oppia.test import OppiaTestCase


class UserSearchActivityViewTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']

    def setUp(self):
        super(UserSearchActivityViewTest, self).setUp()
        self.template = 'profile/users-paginated-list.html'
        self.url = reverse('profile:list')

    def test_view_export(self):

        allowed_users = [self.admin_user, self.staff_user]
        disallowed_users = [self.teacher_user, self.normal_user]

        for allowed_user in allowed_users:
            self.client.force_login(user=allowed_user)
            response = self.client.get(self.url)
            self.assertTemplateUsed(response, self.template)
            self.assertEqual(response.status_code, 200)

        for disallowed_user in disallowed_users:
            self.client.force_login(user=disallowed_user)
            response = self.client.get(self.url)
            self.assertRedirects(response,
                                 '/admin/login/?next=' + self.url,
                                 302,
                                 200)
