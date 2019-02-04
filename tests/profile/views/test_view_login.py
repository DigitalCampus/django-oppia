
from django.urls import reverse
from django.test import TestCase

from django.contrib.auth.models import User

from tests.user_logins import *

class LoginViewTest(TestCase):
    fixtures = ['tests/test_user.json', 
                'tests/test_oppia.json', 
                'tests/test_quiz.json', 
                'tests/test_permissions.json',
                'tests/test_cohort.json']

    def setUp(self):
        super(LoginViewTest, self).setUp()
        
    def test_already_logged_in_admin(self):        
        self.client.login(username=ADMIN_USER['user'], password=ADMIN_USER['password'])
        response = self.client.get(reverse('profile_login'))
        self.assertRedirects(response, reverse('oppia_home'), 302, 200)
            
    def test_already_logged_in_staff(self):        
        self.client.login(username=STAFF_USER['user'], password=STAFF_USER['password'])
        response = self.client.get(reverse('profile_login'))
        self.assertRedirects(response, reverse('oppia_home'), 302, 200)
            
    def test_already_logged_in_teacher(self):        
        self.client.login(username=TEACHER_USER['user'], password=TEACHER_USER['password'])
        response = self.client.get(reverse('profile_login'), follow=True)
        self.assertTemplateUsed(response, 'oppia/home-teacher.html')
        self.assertEqual(response.status_code, 200)
            
    def test_already_logged_in_user(self):        
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        response = self.client.get(reverse('profile_login'), follow=True)
        self.assertTemplateUsed(response, 'oppia/profile/user-scorecard.html')
        self.assertEqual(response.status_code, 200)
        
        
    
        