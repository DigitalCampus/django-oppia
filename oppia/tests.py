# oppia/tests.py
from django.test import TestCase
from django.test.client import Client

from tastypie.test import ResourceTestCase

class BasicTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_register(self):
        response = self.client.post('/profile/register/', {'username': 'demo', 'password': 'secret', 'password_again':'secret', 'email':'demo@demo.com', 'first_name':'demo','last_name':'user'})
        self.assertEqual(response.status_code, 302)
    
    def test_register_with_no_data(self):
        response = self.client.post('/profile/register/', {})
        self.assertEqual(response.status_code, 200)
           
    def test_login(self):
        response = self.client.post('/profile/login/', {'username': 'demo', 'password': 'secret'})
        self.assertEqual(response.status_code, 200)

        
class RegisterResourceTest(ResourceTestCase):    
    def setUp(self):
        super(RegisterResourceTest, self).setUp()
        self.post_data = {
            'username': 'demo2',
            'password': 'secret',
            'email': 'second-post',
        }
        
    def test_get_list_invalid(self):
        # check get method not allowed
        self.assertHttpMethodNotAllowed(self.api_client.get('/api/v1/register/', format='json'))
    
    def test_post_with_invalid_data(self):
        # check posting with not all fields
        data = self.post_data
        self.assertHttpBadRequest(self.api_client.post('/api/v1/register/', format='json', data=self.post_data))

# TODO add tests for ...
# ActivityScheduleResource
# AwardsResource
# BadgesResource
# CourseResource
# CourseTagResource
# ModuleResource
# PointsResource
# PointsResource
# ScheduleResource
# ScorecardResource
# TagResource
# TrackerResource
# UserResource

# QuizResource
# QuizQuestionResource
# QuestionResource
# QuestionPropsResource
# ResponseResource
# ResponsePropsResource
# QuizPropsResource
# QuizPropsResource
# QuizAttemptResource






