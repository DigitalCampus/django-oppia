
import json
import pytest
import unittest

from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url


class ProgressResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'default_gamification_events.json',
                'tests/awards/award-course.json',
                'tests/test_course_permissions.json',
                'tests/test_cohort.json',
                'tests/test_progress_summary.json']
    
    def setUp(self):
        super(ProgressResourceTest, self).setUp()
        self.user = User.objects.get(username='demo')
        self.admin = User.objects.get(username='admin')
        self.staff = User.objects.get(username='staff')
        self.teacher = User.objects.get(username='teacher')
        self.user_auth = {
            'username': 'demo',
            'api_key': get_api_key(user=self.user).key,
        }
        self.admin_auth = {
            'username': 'admin',
            'api_key': get_api_key(user=self.admin).key
        }
        self.staff_auth = {
            'username': 'staff',
            'api_key': get_api_key(user=self.staff).key
        }
        self.teacher_auth = {
            'username': 'teacher',
            'api_key': get_api_key(user=self.teacher).key
        }
        self.url = get_api_url('v2', 'progress')
    
    def check_json_content(self, json):
        self.assertTrue('shortname' in json)
        self.assertTrue('title' in json)
        self.assertTrue('points' in json)
        self.assertTrue('total_activity' in json)
        self.assertTrue('quizzes_passed' in json)
        self.assertTrue('badges_achieved' in json)
        self.assertTrue('media_viewed' in json)
        self.assertTrue('completed_activities' in json)
        self.assertTrue('percent_complete' in json)
    
    # post disallowed
    def test_post_invalid(self):
        self.assertHttpMethodNotAllowed(
            self.api_client.post(self.url, format='json', data=self.admin_auth))
    
    # admin gets own
    def test_admin_gets_own(self):
        url = self.url + "admin/"
        response = self.api_client.get(
            url, format='json', data=self.admin_auth)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        content = json.loads(response.content)
        self.assertEqual(2, len(content))
        self.check_json_content(content[0])
        
    # staff gets own
    def test_staff_gets_own(self):
        url = self.url + "staff/"
        response = self.api_client.get(
            url, format='json', data=self.staff_auth)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        content = json.loads(response.content)
        self.assertEqual(2, len(content))
        self.check_json_content(content[0])
        
    # teacher gets own
    def test_teacher_gets_own(self):
        url = self.url + "teacher/"
        response = self.api_client.get(
            url, format='json', data=self.teacher_auth)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        content = json.loads(response.content)
        self.assertEqual(2, len(content))
        self.check_json_content(content[0])
    
    # user gets own
    def test_user_gets_own(self):
        url = self.url + "demo/"
        response = self.api_client.get(
            url, format='json', data=self.user_auth)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        content = json.loads(response.content)
        self.assertEqual(3, len(content))
        self.check_json_content(content[0])

    # no user specified
    def test_no_user(self):
        response = self.api_client.get(
            self.url, format='json', data=self.user_auth)
        self.assertEqual(400, response.status_code)
        
        
    # can't get a direct summary resource record, will actually look for a user
    def test_ucs_id(self):
        url = self.url + "17/"
        response = self.api_client.get(
            url, format='json', data=self.user_auth)
        self.assertHttpNotFound(response)
        
    # admin gets teacher/staff/user
    def test_admin_other_users(self):
        url = self.url + "demo/"
        response = self.api_client.get(
            url, format='json', data=self.admin_auth)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        content = json.loads(response.content)
        self.assertEqual(3, len(content))
        self.check_json_content(content[0])
        
        url = self.url + "teacher/"
        response = self.api_client.get(
            url, format='json', data=self.admin_auth)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        content = json.loads(response.content)
        self.assertEqual(2, len(content))
        self.check_json_content(content[0])
        
        url = self.url + "staff/"
        response = self.api_client.get(
            url, format='json', data=self.admin_auth)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        content = json.loads(response.content)
        self.assertEqual(2, len(content))
        self.check_json_content(content[0])
        
    # staff gets admin/teacher/user
    def test_staff_other_users(self):
        url = self.url + "demo/"
        response = self.api_client.get(
            url, format='json', data=self.staff_auth)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        content = json.loads(response.content)
        self.assertEqual(3, len(content))
        self.check_json_content(content[0])
        
        url = self.url + "teacher/"
        response = self.api_client.get(
            url, format='json', data=self.staff_auth)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        content = json.loads(response.content)
        self.assertEqual(2, len(content))
        self.check_json_content(content[0])
        
        url = self.url + "admin/"
        response = self.api_client.get(
            url, format='json', data=self.staff_auth)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        content = json.loads(response.content)
        self.assertEqual(2, len(content))
        self.check_json_content(content[0])
        
    # teacher can't get admin/staff
    def test_teacher_other_users(self):
        url = self.url + "admin/"
        response = self.api_client.get(
            url, format='json', data=self.teacher_auth)
        self.assertHttpNotFound(response)
        
        url = self.url + "staff/"
        response = self.api_client.get(
            url, format='json', data=self.teacher_auth)
        self.assertHttpNotFound(response)
        
        url = self.url + "demo/"
        response = self.api_client.get(
            url, format='json', data=self.teacher_auth)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        content = json.loads(response.content)
        self.assertEqual(1, len(content))
        self.check_json_content(content[0])
        
    # user can;t get admin/teacher/staff
    def test_user_other_users(self):
        url = self.url + "admin/"
        response = self.api_client.get(
            url, format='json', data=self.user_auth)
        self.assertHttpNotFound(response)
        
        url = self.url + "staff/"
        response = self.api_client.get(
            url, format='json', data=self.user_auth)
        self.assertHttpNotFound(response)
        
        url = self.url + "teacher/"
        response = self.api_client.get(
            url, format='json', data=self.user_auth)
        self.assertHttpNotFound(response)
    
    # invalid user
    def test_invalid_user(self):
        url = self.url + "not-a-user/"
        response = self.api_client.get(
            url, format='json', data=self.user_auth)
        self.assertHttpNotFound(response)
        