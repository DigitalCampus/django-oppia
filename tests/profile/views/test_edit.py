
from django import forms
from django.urls import reverse
from django.test import TestCase

from django.contrib.auth.models import User

from tests.user_logins import *

class EditProfileViewTest(TestCase):
    fixtures = ['tests/test_user.json', 
                'tests/test_oppia.json', 
                'tests/test_quiz.json', 
                'tests/test_permissions.json']

    def setUp(self):
        super(EditProfileViewTest, self).setUp()
    
    def test_view_own_profile(self):
        
        # admin
        self.client.login(username=ADMIN_USER['user'], password=ADMIN_USER['password'])
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
        
        # staff
        self.client.login(username=STAFF_USER['user'], password=STAFF_USER['password'])
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
        
        # teacher
        self.client.login(username=TEACHER_USER['user'], password=TEACHER_USER['password'])
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
        
        # user    
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
     
    def test_view_others_profile_admin(self): 
        
        # admin
        self.client.login(username=ADMIN_USER['user'], password=ADMIN_USER['password'])
        response = self.client.get(reverse('profile_edit_user',args=[2]))
        self.assertEqual(response.status_code, 200)  
        
        response = self.client.get(reverse('profile_edit_user',args=[3]))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('profile_edit_user',args=[4]))
        self.assertEqual(response.status_code, 200)   
    
    def test_view_others_profile_staff(self):    
        # staff
        self.client.login(username=STAFF_USER['user'], password=STAFF_USER['password'])
        response = self.client.get(reverse('profile_edit_user',args=[1]))
        self.assertEqual(response.status_code, 200)  
        
        response = self.client.get(reverse('profile_edit_user',args=[2]))
        self.assertEqual(response.status_code, 200) 
        
        response = self.client.get(reverse('profile_edit_user',args=[4]))
        self.assertEqual(response.status_code, 200) 
    
    
    def test_view_others_profile_teacher(self):    
        # teacher
        self.client.login(username=TEACHER_USER['user'], password=TEACHER_USER['password'])
        response = self.client.get(reverse('profile_edit_user',args=[1]))
        self.assertEqual(response.status_code, 403)  
        
        response = self.client.get(reverse('profile_edit_user',args=[2]))
        self.assertEqual(response.status_code, 403) 
        
        response = self.client.get(reverse('profile_edit_user',args=[3]))
        self.assertEqual(response.status_code, 403)    
        
        
    def test_view_others_profile_user(self):    
        # user
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        response = self.client.get(reverse('profile_edit_user',args=[1]))
        self.assertEqual(response.status_code, 403)  
        
        response = self.client.get(reverse('profile_edit_user',args=[2]))
        self.assertEqual(response.status_code, 403) 
        
        response = self.client.get(reverse('profile_edit_user',args=[3]))
        self.assertEqual(response.status_code, 403) 
    
    def test_edit_own_profile_admin(self):
        orig_org = User.objects.get(username=ADMIN_USER['user']).userprofile.organisation
        new_org = 'my organisation'
        self.client.login(username=ADMIN_USER['user'], password=ADMIN_USER['password'])
        post_data = {'organisation': new_org,
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user'}
        response = self.client.post(reverse('profile_edit'), data=post_data)
        self.assertEqual(response.status_code, 200)
           
        new_org = User.objects.get(username=ADMIN_USER['user']).userprofile.organisation
        self.assertNotEqual(orig_org,new_org)
    
    def test_edit_own_profile_staff(self):
        orig_org = User.objects.get(username=STAFF_USER['user']).userprofile.organisation
        new_org = 'my organisation'
        self.client.login(username=STAFF_USER['user'], password=STAFF_USER['password'])
        post_data = {'organisation': new_org,
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user'}
        response = self.client.post(reverse('profile_edit'), data=post_data)
        self.assertEqual(response.status_code, 200)
        
        new_org = User.objects.get(username=STAFF_USER['user']).userprofile.organisation
        self.assertNotEqual(orig_org,new_org)
        
    def test_edit_own_profile_teacher(self):
        orig_org = User.objects.get(username=TEACHER_USER['user']).userprofile.organisation
        new_org = 'my organisation'
        self.client.login(username=TEACHER_USER['user'], password=TEACHER_USER['password'])
        post_data = {'organisation': new_org,
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user'}
        response = self.client.post(reverse('profile_edit'), data=post_data)
        self.assertEqual(response.status_code, 200)
        
        new_org = User.objects.get(username=TEACHER_USER['user']).userprofile.organisation
        self.assertNotEqual(orig_org,new_org)
    
    def test_edit_own_profile_user(self):
        orig_org = User.objects.get(username=NORMAL_USER['user']).userprofile.organisation
        new_org = 'my organisation'
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        post_data = {'organisation': new_org,
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user'}
        response = self.client.post(reverse('profile_edit'), data=post_data)
        self.assertEqual(response.status_code, 200)
        
        new_org = User.objects.get(username=NORMAL_USER['user']).userprofile.organisation
        self.assertNotEqual(orig_org,new_org)
    
    def test_edit_others_profile_admin(self):
        orig_org = User.objects.get(username=NORMAL_USER['user']).userprofile.organisation
        new_org = 'my organisation'
        self.client.login(username=ADMIN_USER['user'], password=ADMIN_USER['password'])
        post_data = {'organisation': new_org,
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user'}
        response = self.client.post(reverse('profile_edit_user',args=[2]), data=post_data)
        self.assertEqual(response.status_code, 200)
        
        new_org = User.objects.get(username=NORMAL_USER['user']).userprofile.organisation
        self.assertNotEqual(orig_org,new_org)
    
    def test_edit_others_profile_staff(self):
        orig_org = User.objects.get(username=NORMAL_USER['user']).userprofile.organisation
        new_org = 'my organisation'
        self.client.login(username=STAFF_USER['user'], password=STAFF_USER['password'])
        post_data = {'organisation': new_org,
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user'}
        response = self.client.post(reverse('profile_edit_user',args=[2]), data=post_data)
        self.assertEqual(response.status_code, 200)
        
        new_org = User.objects.get(username=NORMAL_USER['user']).userprofile.organisation
        self.assertNotEqual(orig_org,new_org)
            
    def test_edit_others_profile_teacher(self):
        orig_org = User.objects.get(username=NORMAL_USER['user']).userprofile.organisation
        new_org = 'my organisation'
        self.client.login(username=TEACHER_USER['user'], password=TEACHER_USER['password'])
        post_data = {'organisation': new_org,
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user'}
        response = self.client.post(reverse('profile_edit_user',args=[2]), data=post_data)
        self.assertEqual(response.status_code, 403)
        
        new_org = User.objects.get(username=NORMAL_USER['user']).userprofile.organisation
        self.assertEqual(orig_org,new_org)
    
    def test_edit_others_profile_user(self):
        orig_org = User.objects.get(username=ADMIN_USER['user']).userprofile.organisation
        new_org = 'my organisation'
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        post_data = {'organisation': new_org,
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user'}
        response = self.client.post(reverse('profile_edit_user',args=[1]), data=post_data)
        self.assertEqual(response.status_code, 403)
        
        new_org = User.objects.get(username=ADMIN_USER['user']).userprofile.organisation
        self.assertEqual(orig_org,new_org)
    
    def test_edit_own_password_admin(self):
        self.client.login(username=ADMIN_USER['user'], password=ADMIN_USER['password'])
        post_data = {'organisation': '',
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user',
                     'password': 'newpassword',
                     'password_again': 'newpassword'}
        response = self.client.post(reverse('profile_edit'), data=post_data)
        self.assertEqual(response.status_code, 200)
        
        self.client.login(username=ADMIN_USER['user'], password=ADMIN_USER['password'])
        response = self.client.get(reverse('profile_edit'))
        self.assertRedirects(response, reverse('profile_login') + "?next=" + reverse('profile_edit'), 302, 200)
        
        self.client.login(username=ADMIN_USER['user'], password='newpassword')
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
        
    def test_edit_own_password_staff(self):
        self.client.login(username=STAFF_USER['user'], password=STAFF_USER['password'])
        post_data = {'organisation': '',
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user',
                     'password': 'newpassword',
                     'password_again': 'newpassword'}
        response = self.client.post(reverse('profile_edit'), data=post_data)
        self.assertEqual(response.status_code, 200)
        
        self.client.login(username=STAFF_USER['user'], password=STAFF_USER['password'])
        response = self.client.get(reverse('profile_edit'))
        self.assertRedirects(response, reverse('profile_login') + "?next=" + reverse('profile_edit'), 302, 200)
        
        self.client.login(username=STAFF_USER['user'], password='newpassword')
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
        
    def test_edit_own_password_teacher(self):
        self.client.login(username=TEACHER_USER['user'], password=TEACHER_USER['password'])
        post_data = {'organisation': '',
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user',
                     'password': 'newpassword',
                     'password_again': 'newpassword'}
        response = self.client.post(reverse('profile_edit'), data=post_data)
        self.assertEqual(response.status_code, 200)
        
        self.client.login(username=TEACHER_USER['user'], password=TEACHER_USER['password'])
        response = self.client.get(reverse('profile_edit'))
        self.assertRedirects(response, reverse('profile_login') + "?next=" + reverse('profile_edit'), 302, 200)
        
        self.client.login(username=TEACHER_USER['user'], password='newpassword')
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
        
    def test_edit_own_password_user(self):
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        post_data = {'organisation': '',
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user',
                     'password': 'newpassword',
                     'password_again': 'newpassword'}
        response = self.client.post(reverse('profile_edit'), data=post_data)
        self.assertEqual(response.status_code, 200)
        
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        response = self.client.get(reverse('profile_edit'))
        self.assertRedirects(response, reverse('profile_login') + "?next=" + reverse('profile_edit'), 302, 200)
        
        self.client.login(username=NORMAL_USER['user'], password='newpassword')
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
    
    
    def test_edit_other_password_admin(self):
        self.client.login(username=ADMIN_USER['user'], password=ADMIN_USER['password'])
        post_data = {'organisation': '',
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user',
                     'password': 'newpassword',
                     'password_again': 'newpassword'}
        response = self.client.post(reverse('profile_edit_user', args=[2]), data=post_data)
        self.assertEqual(response.status_code, 200)
        
        self.client.login(username=NORMAL_USER['user'], password='newpassword')
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)   
     
    def test_edit_other_password_staff(self):
        self.client.login(username=STAFF_USER['user'], password=STAFF_USER['password'])
        post_data = {'organisation': '',
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user',
                     'password': 'newpassword',
                     'password_again': 'newpassword'}
        response = self.client.post(reverse('profile_edit_user', args=[2]), data=post_data)
        self.assertEqual(response.status_code, 200)
        
        self.client.login(username=NORMAL_USER['user'], password='newpassword')
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)   
    
    def test_edit_other_password_teacher(self):
        self.client.login(username=TEACHER_USER['user'], password=TEACHER_USER['password'])
        post_data = {'organisation': '',
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user',
                     'password': 'newpassword',
                     'password_again': 'newpassword'}
        response = self.client.post(reverse('profile_edit_user', args=[2]), data=post_data)
        self.assertEqual(response.status_code, 403)    
     
    def test_edit_other_password_user(self):
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        post_data = {'organisation': '',
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user',
                     'password': 'newpassword',
                     'password_again': 'newpassword'}
        response = self.client.post(reverse('profile_edit_user', args=[1]), data=post_data)
        self.assertEqual(response.status_code, 403)  
        
    def test_edit_own_password_user(self):
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        post_data = {'organisation': '',
                     'email': 'admin@me.com',
                     'username': 'admin',
                     'first_name': 'admin',
                     'last_name': 'user',
                     'password': 'newpassword',
                     'password_again': 'somethingelsepassword'}
        self.client.post(reverse('profile_edit'), data=post_data)
        self.assertRaisesMessage(forms.ValidationError, 'Passwords do not match')  
        
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)   
      
    def test_edit_existing_email(self):
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        post_data = {'organisation': '',
                     'email': 'admin@me.com',
                     'username': 'user',
                     'first_name': 'demo',
                     'last_name': 'user'}
        self.client.post(reverse('profile_edit'), data=post_data)
        self.assertRaisesMessage(forms.ValidationError, 'Email address already in use')  
             
    def test_delete_account_admin(self):
        self.client.login(username=ADMIN_USER['user'], password=ADMIN_USER['password'])
        post_data = { 'username': 'admin', 'password': 'password' }
        response = self.client.post(reverse('profile_delete_account'), data=post_data)
        self.assertRedirects(response, reverse('profile_delete_account_complete'), 302, 200)
        
    def test_delete_account_staff(self):
        self.client.login(username=STAFF_USER['user'], password=STAFF_USER['password'])
        post_data = { 'username': 'staff', 'password': 'password' }
        response = self.client.post(reverse('profile_delete_account'), data=post_data)
        self.assertRedirects(response, reverse('profile_delete_account_complete'), 302, 200)
     
    def test_delete_account_teacher(self):
        self.client.login(username=TEACHER_USER['user'], password=TEACHER_USER['password'])
        post_data = { 'username': 'teacher', 'password': 'password' }
        response = self.client.post(reverse('profile_delete_account'), data=post_data)
        self.assertRedirects(response, reverse('profile_delete_account_complete'), 302, 200)   
     
    def test_delete_account_user(self):
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        post_data = { 'username': 'demo', 'password': 'password' }
        response = self.client.post(reverse('profile_delete_account'), data=post_data)
        self.assertRedirects(response, reverse('profile_delete_account_complete'), 302, 200)    
     
    def test_delete_account_wrong_password(self):
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        post_data = { 'username': 'demo', 'password': 'wrongpassword' }
        self.client.post(reverse('profile_delete_account'), data=post_data)
        self.assertRaisesMessage(forms.ValidationError, 'Invalid password. Please try again. ') 
    
    def test_export_data_activity_user(self):
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        response = self.client.get(reverse('profile_export_mydata', args=['activity']))
        self.assertTemplateUsed(response, 'oppia/profile/export/activity.html')
        self.assertEqual(response.status_code, 200)       
    
    def test_export_data_quiz_user(self):    
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        response = self.client.get(reverse('profile_export_mydata', args=['quiz']))
        self.assertTemplateUsed(response, 'oppia/profile/export/quiz_attempts.html')
        self.assertEqual(response.status_code, 200)   
     
    def test_export_data_points_user(self):    
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        response = self.client.get(reverse('profile_export_mydata', args=['points']))
        self.assertTemplateUsed(response, 'oppia/profile/export/points.html')
        self.assertEqual(response.status_code, 200)  
    
    def test_export_data_badges_user(self):        
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        response = self.client.get(reverse('profile_export_mydata', args=['badges']))
        self.assertTemplateUsed(response, 'oppia/profile/export/badges.html')
        self.assertEqual(response.status_code, 200)  
    
    def test_export_data_other_user(self):     
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        response = self.client.get(reverse('profile_export_mydata', args=['somethingelse']))
        self.assertEqual(response.status_code, 404) 
