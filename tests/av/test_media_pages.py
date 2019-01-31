from django.test import TestCase

from tests.utils import *


class AVPagesViewTest(TestCase):
    fixtures = ['tests/test_user.json', 
                'tests/test_oppia.json', 
                'tests/test_quiz.json', 
                'tests/test_permissions.json']

    def setUp(self):
        super(AVPagesViewTest, self).setUp()
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
        
    def test_home_view(self):   
        url = reverse('oppia_av_home')
        allowed_users = [self.admin_user, self.teacher_user, self.staff_user, self.normal_user]
        
        for allowed_user in allowed_users:
            self.client.login(username=allowed_user['user'], password=allowed_user['password'])
            response = self.client.get(url)
            self.assertTemplateUsed(response, 'oppia/av/home.html')
            self.assertEqual(response.status_code, 200)
            
    #  TODO:
    # test viewing AV page (need to add sample data for this)
    # test set_as_default image (and who can view/do this - admin/staff only?)