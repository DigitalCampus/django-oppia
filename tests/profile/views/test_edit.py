from django.urls import reverse
from django.test import TestCase


class EditProfileViewTest(TestCase):
    fixtures = ['tests/test_user.json', 
                'tests/test_oppia.json', 
                'tests/test_quiz.json', 
                'tests/test_permissions.json']

    def setUp(self):
        super(EditProfileViewTest, self).setUp()
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
    
    def test_view_own_profile(self):
        
        # admin
        self.client.login(username=self.admin_user['user'], password=self.admin_user['password'])
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
        
        # staff
        self.client.login(username=self.staff_user['user'], password=self.staff_user['password'])
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
        
        # teacher
        self.client.login(username=self.teacher_user['user'], password=self.teacher_user['password'])
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
        
        # user    
        self.client.login(username=self.normal_user['user'], password=self.normal_user['password'])
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
     
    def test_view_others_profile_admin(self): 
        
        # admin
        self.client.login(username=self.admin_user['user'], password=self.admin_user['password'])
        response = self.client.get(reverse('profile_edit_user',args=[2]))
        self.assertEqual(response.status_code, 200)  
        
        response = self.client.get(reverse('profile_edit_user',args=[3]))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('profile_edit_user',args=[4]))
        self.assertEqual(response.status_code, 200)   
    
    def test_view_others_profile_staff(self):    
        # staff
        self.client.login(username=self.staff_user['user'], password=self.staff_user['password'])
        response = self.client.get(reverse('profile_edit_user',args=[1]))
        self.assertEqual(response.status_code, 200)  
        
        response = self.client.get(reverse('profile_edit_user',args=[2]))
        self.assertEqual(response.status_code, 200) 
        
        response = self.client.get(reverse('profile_edit_user',args=[4]))
        self.assertEqual(response.status_code, 200) 
    
    
    def test_view_others_profile_teacher(self):    
        # teacher
        self.client.login(username=self.teacher_user['user'], password=self.teacher_user['password'])
        response = self.client.get(reverse('profile_edit_user',args=[1]))
        self.assertEqual(response.status_code, 403)  
        
        response = self.client.get(reverse('profile_edit_user',args=[2]))
        self.assertEqual(response.status_code, 403) 
        
        response = self.client.get(reverse('profile_edit_user',args=[3]))
        self.assertEqual(response.status_code, 403)    
        
        
    def test_view_others_profile_user(self):    
        # user
        self.client.login(username=self.normal_user['user'], password=self.normal_user['password'])
        response = self.client.get(reverse('profile_edit_user',args=[1]))
        self.assertEqual(response.status_code, 403)  
        
        response = self.client.get(reverse('profile_edit_user',args=[2]))
        self.assertEqual(response.status_code, 403) 
        
        response = self.client.get(reverse('profile_edit_user',args=[3]))
        self.assertEqual(response.status_code, 403) 
        
'''
- view profile page
- admin being able to edit another users account
- reset password
- update personal data
- not being able to change username or api key
- changing to existing email
- delete account (but only own)
- export data (but only own)
'''