
from django import forms
from django.urls import reverse
from django.test import TestCase

from django.contrib.auth.models import User

from tests.user_logins import *

class PointsViewTest(TestCase):
    fixtures = ['tests/test_user.json', 
                'tests/test_oppia.json', 
                'tests/test_quiz.json', 
                'tests/test_permissions.json']

    def setUp(self):
        super(PointsViewTest, self).setUp()
        
    def test_view_badges(self):
        url = reverse('profile_points')
        allowed_users = [ADMIN_USER, STAFF_USER, TEACHER_USER, NORMAL_USER]
        
        for allowed_user in allowed_users:
            self.client.login(username=allowed_user['user'], password=allowed_user['password'])
            response = self.client.get(url)
            self.assertTemplateUsed(response, 'oppia/profile/points.html')
            self.assertEqual(response.status_code, 200)
        
        