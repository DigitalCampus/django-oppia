from django.urls import reverse
from oppia.test import OppiaTestCase


class UserActivityViewTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']

    def setUp(self):
        super(UserActivityViewTest, self).setUp()
        self.template = 'profile/user-scorecard.html'
        self.unauthorised_template = '403.html'

    def test_view_own_activity(self):

        allowed_users = [self.admin_user,
                         self.staff_user,
                         self.teacher_user,
                         self.normal_user]

        for allowed_user in allowed_users:
            url = reverse('profile:user_activity', args=[allowed_user.id])
            self.client.force_login(allowed_user)
            response = self.client.get(url)
            self.assertTemplateUsed(response, self.template)
            self.assertEqual(response.status_code, 200)

    def test_admin_view_others_activity(self):
        url = reverse('profile:user_activity', args=[self.staff_user.id])
        self.client.force_login(self.admin_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

        url = reverse('profile:user_activity', args=[self.teacher_user.id])
        self.client.force_login(self.admin_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

        url = reverse('profile:user_activity', args=[self.normal_user.id])
        self.client.force_login(self.admin_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

    def test_staff_view_others_activity(self):
        url = reverse('profile:user_activity', args=[self.admin_user.id])
        self.client.force_login(self.staff_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

        url = reverse('profile:user_activity', args=[self.teacher_user.id])
        self.client.force_login(self.staff_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

        url = reverse('profile:user_activity', args=[self.normal_user.id])
        self.client.force_login(self.staff_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)

    def test_teacher_view_others_activity(self):
        url = reverse('profile:user_activity', args=[self.admin_user.id])
        self.client.force_login(self.teacher_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, '403.html')
        self.assertEqual(response.status_code, 403)

        url = reverse('profile:user_activity', args=[self.staff_user.id])
        self.client.force_login(self.teacher_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.unauthorised_template)
        self.assertEqual(response.status_code, 403)

        url = reverse('profile:user_activity', args=[self.normal_user.id])
        self.client.force_login(self.teacher_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.unauthorised_template)
        self.assertEqual(response.status_code, 403)

    def test_user_view_others_activity(self):
        url = reverse('profile:user_activity', args=[self.admin_user.id])
        self.client.force_login(self.normal_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.unauthorised_template)
        self.assertEqual(response.status_code, 403)

        url = reverse('profile:user_activity', args=[self.staff_user.id])
        self.client.force_login(self.normal_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.unauthorised_template)
        self.assertEqual(response.status_code, 403)

        url = reverse('profile:user_activity', args=[self.teacher_user.id])
        self.client.force_login(self.normal_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.unauthorised_template)
        self.assertEqual(response.status_code, 403)
