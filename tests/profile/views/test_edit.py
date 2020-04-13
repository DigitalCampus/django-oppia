
from django import forms
from django.urls import reverse
from oppia.test import OppiaTestCase

from django.contrib.auth.models import User


class EditProfileViewTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']

    def test_view_own_profile(self):

        # admin
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('profile:edit'))
        self.assertEqual(response.status_code, 200)

        # staff
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse('profile:edit'))
        self.assertEqual(response.status_code, 200)

        # teacher
        self.client.force_login(self.teacher_user)
        response = self.client.get(reverse('profile:edit'))
        self.assertEqual(response.status_code, 200)

        # user
        self.client.force_login(self.normal_user)
        response = self.client.get(reverse('profile:edit'))
        self.assertEqual(response.status_code, 200)

    def test_view_others_profile_admin(self):

        # admin
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('profile:edit_user', args=[2]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('profile:edit_user', args=[3]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('profile:edit_user', args=[4]))
        self.assertEqual(response.status_code, 200)

    def test_view_others_profile_staff(self):
        # staff
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse('profile:edit_user', args=[1]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('profile:edit_user', args=[2]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('profile:edit_user', args=[4]))
        self.assertEqual(response.status_code, 200)

    def test_view_others_profile_teacher(self):
        # teacher
        self.client.force_login(self.teacher_user)
        response = self.client.get(reverse('profile:edit_user', args=[1]))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse('profile:edit_user', args=[2]))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse('profile:edit_user', args=[3]))
        self.assertEqual(response.status_code, 403)

    def test_view_others_profile_user(self):
        # user
        self.client.force_login(self.normal_user)
        response = self.client.get(reverse('profile:edit_user', args=[1]))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse('profile:edit_user', args=[2]))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse('profile:edit_user', args=[3]))
        self.assertEqual(response.status_code, 403)

    def test_edit_own_profile_admin(self):
        orig_org = User.objects.get(
            username=self.admin_user.username).userprofile.organisation
        new_org = 'my organisation'
        self.client.force_login(self.admin_user)
        post_data = {'organisation': new_org,
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user'}
        response = self.client.post(
            reverse('profile:edit'), data=post_data)
        self.assertEqual(response.status_code, 200)

        new_org = User.objects.get(
            username=self.admin_user.username).userprofile.organisation
        self.assertNotEqual(orig_org, new_org)

    def test_edit_own_profile_staff(self):
        orig_org = User.objects.get(
            username=self.staff_user.username).userprofile.organisation
        new_org = 'my organisation'
        self.client.force_login(self.staff_user)
        post_data = {'organisation': new_org,
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user'}
        response = self.client.post(reverse('profile:edit'), data=post_data)
        self.assertEqual(response.status_code, 200)

        new_org = User.objects.get(
            username=self.staff_user.username).userprofile.organisation
        self.assertNotEqual(orig_org, new_org)

    def test_edit_own_profile_teacher(self):
        orig_org = User.objects.get(
            username=self.teacher_user.username).userprofile.organisation
        new_org = 'my organisation'
        self.client.force_login(self.teacher_user)
        post_data = {'organisation': new_org,
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user'}
        response = self.client.post(reverse('profile:edit'), data=post_data)
        self.assertEqual(response.status_code, 200)

        new_org = User.objects.get(
            username=self.teacher_user.username).userprofile.organisation
        self.assertNotEqual(orig_org, new_org)

    def test_edit_own_profile_user(self):
        orig_org = User.objects.get(
            username=self.normal_user.username).userprofile.organisation
        new_org = 'my organisation'
        self.client.force_login(self.normal_user)
        post_data = {'organisation': new_org,
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user'}
        response = self.client.post(reverse('profile:edit'), data=post_data)
        self.assertEqual(response.status_code, 200)

        new_org = User.objects.get(
            username=self.normal_user.username).userprofile.organisation
        self.assertNotEqual(orig_org, new_org)

    def test_edit_others_profile_admin(self):
        orig_org = User.objects.get(
            username=self.normal_user.username).userprofile.organisation
        new_org = 'my organisation'
        self.client.force_login(self.admin_user)
        post_data = {'organisation': new_org,
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user'}
        response = self.client.post(reverse('profile:edit_user',
                                            args=[2]), data=post_data)
        self.assertEqual(response.status_code, 200)

        new_org = User.objects.get(
            username=self.normal_user.username).userprofile.organisation
        self.assertNotEqual(orig_org, new_org)

    def test_edit_others_profile_staff(self):
        orig_org = User.objects.get(
            username=self.normal_user.username).userprofile.organisation
        new_org = 'my organisation'
        self.client.force_login(self.staff_user)
        post_data = {'organisation': new_org,
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user'}
        response = self.client.post(reverse('profile:edit_user',
                                            args=[2]), data=post_data)
        self.assertEqual(response.status_code, 200)

        new_org = User.objects.get(
            username=self.normal_user.username).userprofile.organisation
        self.assertNotEqual(orig_org, new_org)

    def test_edit_others_profile_teacher(self):
        orig_org = User.objects.get(
            username=self.normal_user.username).userprofile.organisation
        new_org = 'my organisation'
        self.client.force_login(self.teacher_user)
        post_data = {'organisation': new_org,
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user'}
        response = self.client.post(reverse('profile:edit_user',
                                            args=[2]), data=post_data)
        self.assertEqual(response.status_code, 403)

        new_org = User.objects.get(
            username=self.normal_user.username).userprofile.organisation
        self.assertEqual(orig_org, new_org)

    def test_edit_others_profile_user(self):
        orig_org = User.objects.get(
            username=self.admin_user.username).userprofile.organisation
        new_org = 'my organisation'
        self.client.force_login(self.normal_user)
        post_data = {'organisation': new_org,
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user'}
        response = self.client.post(reverse('profile:edit_user',
                                            args=[1]), data=post_data)
        self.assertEqual(response.status_code, 403)

        new_org = User.objects.get(
            username=self.admin_user.username).userprofile.organisation
        self.assertEqual(orig_org, new_org)

    def test_edit_own_password_admin(self):
        self.client.force_login(self.admin_user)
        post_data = {'organisation': '',
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user',
                     'password': 'newpassword',
                     'password_again': 'newpassword'}
        response = self.client.post(reverse('profile:edit'), data=post_data)
        self.assertEqual(response.status_code, 200)

        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('profile:edit'))
        self.assertRedirects(response,
                             self.login_url
                             + "?next="
                             + reverse('profile:edit'), 302, 200)

        self.client.login(username=self.admin_user.username,
                          password='newpassword')
        response = self.client.get(reverse('profile:edit'))
        self.assertEqual(response.status_code, 200)

    def test_edit_own_password_staff(self):
        self.client.force_login(self.staff_user)
        post_data = {'organisation': '',
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user',
                     'password': 'newpassword',
                     'password_again': 'newpassword'}
        response = self.client.post(reverse('profile:edit'), data=post_data)
        self.assertEqual(response.status_code, 200)

        self.client.force_login(self.staff_user)
        response = self.client.get(reverse('profile:edit'))
        self.assertRedirects(response,
                             self.login_url
                             + "?next=" +
                             reverse('profile:edit'), 302, 200)

        self.client.login(username=self.staff_user.username,
                          password='newpassword')
        response = self.client.get(reverse('profile:edit'))
        self.assertEqual(response.status_code, 200)

    def test_edit_own_password_teacher(self):
        self.client.force_login(self.teacher_user)
        post_data = {'organisation': '',
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user',
                     'password': 'newpassword',
                     'password_again': 'newpassword'}
        response = self.client.post(reverse('profile:edit'), data=post_data)
        self.assertEqual(response.status_code, 200)

        self.client.force_login(self.teacher_user)
        response = self.client.get(reverse('profile:edit'))
        self.assertRedirects(response,
                             self.login_url
                             + "?next="
                             + reverse('profile:edit'), 302, 200)

        self.client.login(username=self.teacher_user.username,
                          password='newpassword')
        response = self.client.get(reverse('profile:edit'))
        self.assertEqual(response.status_code, 200)

    def test_edit_own_password_user(self):
        self.client.force_login(self.normal_user)
        post_data = {'organisation': '',
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user',
                     'password': 'newpassword',
                     'password_again': 'newpassword'}
        response = self.client.post(reverse('profile:edit'), data=post_data)
        self.assertEqual(response.status_code, 200)

        self.client.force_login(self.normal_user)
        response = self.client.get(reverse('profile:edit'))
        self.assertRedirects(response,
                             self.login_url
                             + "?next="
                             + reverse('profile:edit'), 302, 200)

        self.client.login(username=self.normal_user.username,
                          password='newpassword')
        response = self.client.get(reverse('profile:edit'))
        self.assertEqual(response.status_code, 200)

    def test_edit_other_password_admin(self):
        self.client.force_login(self.admin_user)
        post_data = {'organisation': '',
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user',
                     'password': 'newpassword',
                     'password_again': 'newpassword'}
        response = self.client.post(reverse('profile:edit_user',
                                            args=[2]), data=post_data)
        self.assertEqual(response.status_code, 200)

        self.client.login(username=self.normal_user.username,
                          password='newpassword')
        response = self.client.get(reverse('profile:edit'))
        self.assertEqual(response.status_code, 200)

    def test_edit_other_password_staff(self):
        self.client.force_login(self.staff_user)
        post_data = {'organisation': '',
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user',
                     'password': 'newpassword',
                     'password_again': 'newpassword'}
        response = self.client.post(reverse('profile:edit_user',
                                            args=[2]), data=post_data)
        self.assertEqual(response.status_code, 200)

        self.client.login(username=self.normal_user.username,
                          password='newpassword')
        response = self.client.get(reverse('profile:edit'))
        self.assertEqual(response.status_code, 200)

    def test_edit_other_password_teacher(self):
        self.client.force_login(self.teacher_user)
        post_data = {'organisation': '',
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user',
                     'password': 'newpassword',
                     'password_again': 'newpassword'}
        response = self.client.post(reverse('profile:edit_user',
                                            args=[2]), data=post_data)
        self.assertEqual(response.status_code, 403)

    def test_edit_other_password_user(self):
        self.client.force_login(self.normal_user)
        post_data = {'organisation': '',
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user',
                     'password': 'newpassword',
                     'password_again': 'newpassword'}
        response = self.client.post(reverse('profile:edit_user',
                                            args=[1]), data=post_data)
        self.assertEqual(response.status_code, 403)

    def test_edit_existing_email(self):
        self.client.force_login(self.normal_user)
        post_data = {'organisation': '',
                     'email': 'admin@me.com',
                     'username': 'user',
                     'first_name': 'demo',
                     'last_name': 'user'}
        self.client.post(reverse('profile:edit'), data=post_data)
        self.assertRaisesMessage(forms.ValidationError,
                                 'Email address already in use')

    def test_delete_account_admin(self):
        self.client.force_login(self.admin_user)
        post_data = {'username': 'admin', 'password': 'password'}
        response = self.client.post(reverse('profile:delete',
                                            args=[self.admin_user.id]),
                                    data=post_data)
        self.assertRedirects(response,
                             reverse('profile:delete_complete'),
                             302,
                             200)

    def test_delete_account_staff(self):
        self.client.force_login(self.staff_user)
        post_data = {'username': 'staff', 'password': 'password'}
        response = self.client.post(reverse('profile:delete',
                                            args=[self.staff_user.id]),
                                    data=post_data)
        self.assertRedirects(response,
                             reverse('profile:delete_complete'),
                             302,
                             200)

    def test_delete_account_teacher(self):
        self.client.force_login(self.teacher_user)
        post_data = {'username': 'teacher', 'password': 'password'}
        response = self.client.post(reverse('profile:delete',
                                            args=[self.teacher_user.id]),
                                    data=post_data)
        self.assertRedirects(response,
                             reverse('profile:delete_complete'),
                             302,
                             200)

    def test_delete_account_user(self):
        self.client.force_login(self.normal_user)
        post_data = {'username': 'demo', 'password': 'password'}
        response = self.client.post(reverse('profile:delete',
                                            args=[self.normal_user.id]),
                                    data=post_data)
        self.assertRedirects(response,
                             reverse('profile:delete_complete'),
                             302,
                             200)

    def test_delete_account_user_by_admin(self):
        self.client.force_login(self.admin_user)
        post_data = {'username': 'admin', 'password': 'password'}
        response = self.client.post(reverse('profile:delete',
                                            args=[self.normal_user.id]),
                                    data=post_data)
        self.assertRedirects(response,
                             reverse('profile:delete_complete'),
                             302,
                             200)

    def test_delete_account_user_by_staff(self):
        self.client.force_login(self.staff_user)
        post_data = {'username': 'staff', 'password': 'password'}
        response = self.client.post(reverse('profile:delete',
                                            args=[self.normal_user.id]),
                                    data=post_data)
        self.assertEqual(response.status_code, 403)

    def test_delete_account_user_by_teacher(self):
        self.client.force_login(self.teacher_user)
        post_data = {'username': 'teacher', 'password': 'password'}
        response = self.client.post(reverse('profile:delete',
                                            args=[self.normal_user.id]),
                                    data=post_data)
        self.assertEqual(response.status_code, 403)

    def test_delete_account_user_by_user(self):
        self.client.force_login(self.normal_user)
        post_data = {'username': 'demo', 'password': 'password'}
        response = self.client.post(reverse('profile:delete',
                                            args=[self.teacher_user.id]),
                                    data=post_data)
        self.assertEqual(response.status_code, 403)


    def test_delete_account_wrong_password(self):
        self.client.force_login(self.normal_user)
        post_data = {'username': 'demo', 'password': 'wrongpassword'}
        self.client.post(reverse('profile:delete',
                                 args=[self.normal_user.id]), data=post_data)
        self.assertRaisesMessage(forms.ValidationError,
                                 'Invalid password. Please try again. ')

    def test_export_data_activity_user(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(reverse('profile:export_mydata',
                                           args=['activity']))
        self.assertTemplateUsed(response, 'profile/export/activity.html')
        self.assertEqual(response.status_code, 200)

    def test_export_data_quiz_user(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(reverse('profile:export_mydata',
                                           args=['quiz']))
        self.assertTemplateUsed(response, 'profile/export/quiz_attempts.html')
        self.assertEqual(response.status_code, 200)

    def test_export_data_points_user(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(reverse('profile:export_mydata',
                                           args=['points']))
        self.assertTemplateUsed(response, 'profile/export/points.html')
        self.assertEqual(response.status_code, 200)

    def test_export_data_badges_user(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(reverse('profile:export_mydata',
                                           args=['badges']))
        self.assertTemplateUsed(response, 'profile/export/badges.html')
        self.assertEqual(response.status_code, 200)

    def test_export_data_other_user(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(reverse('profile:export_mydata',
                                           args=['somethingelse']))
        self.assertEqual(response.status_code, 404)
