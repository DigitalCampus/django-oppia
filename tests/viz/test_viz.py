from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from tests.utils import *

from tests.user_logins import *

class VisualisationsTest(TestCase):
    fixtures = ['tests/test_user.json', 
                'tests/test_oppia.json', 
                'tests/test_quiz.json', 
                'tests/test_permissions.json']
    
    def setUp(self):
        super(VisualisationsTest, self).setUp()
        
    # summary
    # only staff/admins can view
    def test_view_summary(self):
        allowed_users = [ADMIN_USER, STAFF_USER]
        disallowed_users = [TEACHER_USER, NORMAL_USER]
    
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
        
        allowed_users = [ADMIN_USER, TEACHER_USER, STAFF_USER, NORMAL_USER]
        
        for allowed_user in allowed_users:
            self.client.login(username=allowed_user['user'], password=allowed_user['password'])
            response = self.client.get(reverse('oppia_viz_map'))
            self.assertTemplateUsed(response, 'oppia/viz/map.html')
            self.assertEqual(response.status_code, 200)
        
    