# oppia/tests/test_site.py
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from tests.utils import *

class OppiaViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home(self):
        response = self.client.get(reverse('oppia_home'))
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.post(reverse('profile_register'), {'username': 'demo', 'password': 'secret', 'password_again': 'secret', 'email': 'demo@demo.com', 'first_name': 'demo', 'last_name': 'user'})
        self.assertEqual(response.status_code, 302)

    def test_register_with_no_data(self):
        response = self.client.post(reverse('profile_register'), {})
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post(reverse('profile_login'), {'username': 'demo', 'password': 'secret'})
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get(reverse('oppia_about'))
        self.assertTemplateUsed(response, 'oppia/about.html')
        self.assertEqual(response.status_code, 200)
    
    def test_server(self):
        response = self.client.get(reverse('oppia_server'))
        self.assertTemplateUsed(response, 'oppia/server.html')
        self.assertEqual(response['Content-Type'], "application/json")
        response.json()
        self.assertIsNotNone(response.json()['version'])
        self.assertIsNotNone(response.json()['name'])
        self.assertIsNotNone(response.json()['admin_email'])
        self.assertIsNotNone(response.json()['max_upload'])
         # check it can load as json object
        self.assertEqual(response.status_code, 200)
    
    # TODO :   
    # course_download_view
    # tag_courses_view
    # add_course_tags
    # recent_activity_detail
    # export_tracker_detail
    # cohort_add
    # cohort_leaderboard_view
    # leaderboard_view
    # course_quiz
    # course_quiz_attempts
    # course_feedback
    # course_feedback_responses
    # app_launch_activity_redirect_view
    
    
    
    
    # TODO test login redirected correctly for all pages
    # except those with login exempt
