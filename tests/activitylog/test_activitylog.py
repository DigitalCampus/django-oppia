# oppia/tests/tracker/test_tracker.py
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from tests.user_logins import *


class UploadActivityLogTest(TestCase):
    
    fixtures = ['tests/test_user.json', 
                'tests/test_oppia.json', 
                'tests/test_quiz.json', 
                'tests/test_permissions.json']
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('oppia_activitylog_upload')
        self.activity_log_file_path = './oppia/fixtures/reference_files/activity_upload_test.json' 

    def test_no_file(self):
        # no file
        self.client.login(username=ADMIN_USER['user'], password=ADMIN_USER['password'])
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        
    def test_correct_file(self):
        self.client.login(username=ADMIN_USER['user'], password=ADMIN_USER['password'])
        with open(self.activity_log_file_path, 'rb') as activity_log_file:
            response = self.client.post(self.url, { 'activity_log_file': activity_log_file })
        
        self.assertEqual(response.status_code, 200)
        
        