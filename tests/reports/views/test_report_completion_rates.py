
from django.urls import reverse
from django.test import TestCase

from django.contrib.auth.models import User

from tests.user_logins import *
from tests.defaults import *

class ReportCompletionRatesViewTest(TestCase):
    fixtures = ['tests/test_user.json', 
                'tests/test_oppia.json', 
                'tests/test_quiz.json', 
                'tests/test_permissions.json',
                'tests/test_cohort.json']

    def setUp(self):
        super(ReportCompletionRatesViewTest, self).setUp() 
        
    def test_view_completion_rates(self):
        template = 'oppia/reports/completion_rates.html'
        url = reverse('oppia_completion_rates')
        allowed_users = [ADMIN_USER, STAFF_USER]
        disallowed_users = [TEACHER_USER, NORMAL_USER]
        
        for allowed_user in allowed_users:
            self.client.login(username=allowed_user['user'], password=allowed_user['password'])
            response = self.client.get(url)
            self.assertTemplateUsed(response, template)
            self.assertEqual(response.status_code, 200)
            
        for disallowed_user in disallowed_users:
            self.client.login(username=disallowed_user['user'], password=disallowed_user['password'])
            response = self.client.get(url)
            self.assertRedirects(response, '/admin/login/?next=' +  url, 302, 200)
    
    def test_view_course_completion_rates_valid_course(self):
        url = reverse('course_completion_rates', args=[1])
        template = 'oppia/reports/course_completion_rates.html'
        allowed_users = [ADMIN_USER, STAFF_USER]
        disallowed_users = [TEACHER_USER, NORMAL_USER]
        
        for allowed_user in allowed_users:
            self.client.login(username=allowed_user['user'], password=allowed_user['password'])
            response = self.client.get(url)
            self.assertTemplateUsed(response, template)
            self.assertEqual(response.status_code, 200)
            
        for disallowed_user in disallowed_users:
            self.client.login(username=disallowed_user['user'], password=disallowed_user['password'])
            response = self.client.get(url)
            self.assertRedirects(response, '/admin/login/?next=' +  url, 302, 200)
            
    def test_view_course_completion_rates_invalid_course(self):
        url = reverse('course_completion_rates', args=[999])
        allowed_users = [ADMIN_USER, STAFF_USER]
        disallowed_users = [TEACHER_USER, NORMAL_USER]
        
        for allowed_user in allowed_users:
            self.client.login(username=allowed_user['user'], password=allowed_user['password'])
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)
            
        for disallowed_user in disallowed_users:
            self.client.login(username=disallowed_user['user'], password=disallowed_user['password'])
            response = self.client.get(url)
            self.assertRedirects(response, '/admin/login/?next=' +  url, 302, 200)
            