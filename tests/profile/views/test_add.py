
from django import forms
from django.urls import reverse
from oppia.test import OppiaTestCase

from django.contrib.auth.models import User

from settings import constants
from settings.models import SettingProperties


class EditProfileViewTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']

    def test_view_add_profile(self):

        # admin
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse('profile:add'))
        self.assertEqual(response.status_code, 200)

        # staff
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse('profile:add'))
        self.assertEqual(response.status_code, 200)

        # teacher
        self.client.force_login(self.teacher_user)
        response = self.client.get(reverse('profile:add'))
        self.assertEqual(response.status_code, 403)

        # user
        self.client.force_login(self.normal_user)
        response = self.client.get(reverse('profile:add'))
        self.assertEqual(response.status_code, 403)
