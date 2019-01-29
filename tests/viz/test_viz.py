from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from tests.utils import *

class VisualisationsTest(TestCase):
    fixtures = ['tests/test_user.json', 
                'tests/test_oppia.json', 
                'tests/test_quiz.json', 
                'tests/test_permissions.json']
    
    def setUp(self):
        super(VisualisationsTest, self).setUp()

        self.admin_user = {
            'user': 'admin',
            'password': 'password'
        }
        self.staff_user = {
            'user': 'staff',
            'password': 'password'
        }
        self.normal_user = {
            'user': 'demo',
            'password': 'password'
        }
        self.teacher_user = {
            'user': 'teacher',
            'password': 'password'
        }  
        
    # summary
    # only staff/admins can view
    def test_view_summary(self):
        allowed_users = [self.admin_user, self.staff_user]
        disallowed_users = [self.teacher_user, self.normal_user]
    
        for allowed_user in allowed_users:
            self.client.login(username=allowed_user['user'], password=allowed_user['password'])
            response = self.client.get(reverse('oppia_viz_summary'))
            
            self.assertTemplateUsed(response, 'oppia/viz/summary.html')
            self.assertEqual(response.status_code, 200)
        

        for disallowed_user in disallowed_users:
            self.client.login(username=disallowed_user['user'], password=disallowed_user['password'])
            response = self.client.get(reverse('oppia_viz_summary'))
            self.assertEqual(response.status_code, 302)
   
    # map 
    def test_view_map(self):
        
        allowed_users = [self.admin_user, self.teacher_user, self.staff_user, self.normal_user]
        
        for allowed_user in allowed_users:
            self.client.login(username=allowed_user['user'], password=allowed_user['password'])
            response = self.client.get(reverse('oppia_viz_map'))
            self.assertTemplateUsed(response, 'oppia/viz/map.html')
            self.assertEqual(response.status_code, 200)
        
    