from django.urls import reverse
from oppia.test import OppiaTestCase


class UserSearchActivityViewTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_customfields.json',
                'tests/test_course_permissions.json']

    url = reverse('profile:users_list')
    template = 'profile/search_user.html'

    def setUp(self):
        super(UserSearchActivityViewTest, self).setUp()
        self.allowed_users = [self.admin_user, self.staff_user]
        self.disallowed_users = [self.teacher_user, self.normal_user]

    def test_view_search_get(self):

        for allowed_user in self.allowed_users:
            self.client.force_login(user=allowed_user)
            response = self.client.get(self.url)
            self.assertTemplateUsed(response, self.template)
            self.assertEqual(response.status_code, 200)

        for disallowed_user in self.disallowed_users:
            self.client.force_login(user=disallowed_user)
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, 403)

    def test_view_search_basic_query(self):
            self.client.force_login(user=self.admin_user)
            url = self.url + '?q=demo'
            response = self.client.get(url)
            user_count = response.context['page_obj'].paginator.count
            self.assertEqual(response.status_code, 200)
            self.assertEqual(user_count, 2)

    def test_view_search_username(self):
            self.client.force_login(user=self.admin_user)
            url = self.url + '?username=demo'
            response = self.client.get(url)
            user_count = response.context['page_obj'].paginator.count
            self.assertEqual(response.status_code, 200)
            self.assertEqual(user_count, 1)

    def test_view_search_staff(self):
            self.client.force_login(user=self.admin_user)
            url = self.url + '?is_staff=on'
            response = self.client.get(url)
            user_count = response.context['page_obj'].paginator.count
            self.assertEqual(response.status_code, 200)
            self.assertEqual(user_count, 2)

    def test_view_search_customfield(self):
            self.client.force_login(user=self.admin_user)
            url = self.url + '?userprofilecustomfield_country=FI'
            response = self.client.get(url)
            user_count = response.context['page_obj'].paginator.count
            self.assertEqual(response.status_code, 200)
            self.assertEqual(user_count, 2)

    def test_view_search_multiple_fields(self):
            self.client.force_login(user=self.admin_user)
            url = self.url + '?userprofilecustomfield_country=FI&first_name=demo'
            response = self.client.get(url)
            user_count = response.context['page_obj'].paginator.count
            self.assertEqual(response.status_code, 200)
            self.assertEqual(user_count, 1)

    def test_view_search_page_123(self):
        self.client.force_login(self.admin_user)
        url = '%s?page=123' % self.url
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)

    def test_view_search_page_abc(self):
        self.client.force_login(self.admin_user)
        url = '%s?page=abc' % self.url
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
