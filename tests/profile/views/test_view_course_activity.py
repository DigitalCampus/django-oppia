from django import forms
from django.urls import reverse
from django.test import TestCase

from django.contrib.auth.models import User

from tests.user_logins import *
from tests.defaults import *

class CourseActivityViewTest(TestCase):
    fixtures = ['tests/test_user.json', 
                'tests/test_oppia.json', 
                'tests/test_quiz.json', 
                'tests/test_permissions.json']

    def setUp(self):
        super(CourseActivityViewTest, self).setUp()
        self.template = 'oppia/profile/user-course-scorecard.html'
        self.course_id = 1
        self.reverse_url = 'profile_user_course_activity'
        
    def test_view_own_course_activity(self):
        
        allowed_users = [ADMIN_USER, STAFF_USER, TEACHER_USER, NORMAL_USER]
        
        for allowed_user in allowed_users:
            url = reverse(self.reverse_url, args=[allowed_user['id'], self.course_id])
            self.client.login(username=allowed_user['user'], password=allowed_user['password'])
            response = self.client.get(url)
            self.assertTemplateUsed(response, self.template )
            self.assertEqual(response.status_code, 200)
            
    def test_admin_view_others_course_activity(self):
        
        url = reverse(self.reverse_url, args=[STAFF_USER['id'], self.course_id])
        self.client.login(username=ADMIN_USER['user'], password=ADMIN_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)
        
        url = reverse(self.reverse_url, args=[TEACHER_USER['id'], self.course_id])
        self.client.login(username=ADMIN_USER['user'], password=ADMIN_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)
        
        url = reverse(self.reverse_url, args=[NORMAL_USER['id'], self.course_id])
        self.client.login(username=ADMIN_USER['user'], password=ADMIN_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)
        
    def test_staff_view_others_course_activity(self):
        
        url = reverse(self.reverse_url, args=[ADMIN_USER['id'], self.course_id])
        self.client.login(username=STAFF_USER['user'], password=STAFF_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)
        
        url = reverse(self.reverse_url, args=[TEACHER_USER['id'], self.course_id])
        self.client.login(username=STAFF_USER['user'], password=STAFF_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)
        
        url = reverse(self.reverse_url, args=[NORMAL_USER['id'], self.course_id])
        self.client.login(username=STAFF_USER['user'], password=STAFF_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, self.template)
        self.assertEqual(response.status_code, 200)
        
    def test_teacher_view_others_course_activity(self):
        
        url = reverse(self.reverse_url, args=[ADMIN_USER['id'], self.course_id])
        self.client.login(username=TEACHER_USER['user'], password=TEACHER_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE )
        self.assertEqual(response.status_code, 403)
        
        url = reverse(self.reverse_url, args=[STAFF_USER['id'], self.course_id])
        self.client.login(username=TEACHER_USER['user'], password=TEACHER_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE )
        self.assertEqual(response.status_code, 403)
        
        url = reverse(self.reverse_url, args=[NORMAL_USER['id'], self.course_id])
        self.client.login(username=TEACHER_USER['user'], password=TEACHER_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE )
        self.assertEqual(response.status_code, 403)
    
    def test_user_view_others_course_activity(self):
        
        url = reverse(self.reverse_url, args=[ADMIN_USER['id'], self.course_id])
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE )
        self.assertEqual(response.status_code, 403)
        
        url = reverse(self.reverse_url, args=[STAFF_USER['id'], self.course_id])
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE )
        self.assertEqual(response.status_code, 403)
        
        url = reverse(self.reverse_url, args=[TEACHER_USER['id'], self.course_id])
        self.client.login(username=NORMAL_USER['user'], password=NORMAL_USER['password'])
        response = self.client.get(url)
        self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE )
        self.assertEqual(response.status_code, 403)