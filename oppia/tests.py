# oppia/tests.py
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from tastypie.models import ApiKey
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
    
    # check get method not allowed  
    def test_get_list_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.get('/api/v1/register/', format='json'))
    
    # check posting with no username
    def test_post_no_username(self):
        data = {
            'password': 'secret',
            'email': 'demo@demo.com',
            'passwordagain': 'secret',
            'firstname': 'demo',
            'lastname': 'user',
        }
        self.assertHttpBadRequest(self.api_client.post('/api/v1/register/', format='json', data=data))
    
    # check posting with no password
    def test_post_no_password(self):
        data = {
            'username': 'demo2',
            'email': 'demo@demo.com',
            'passwordagain': 'secret',
            'firstname': 'demo',
            'lastname': 'user',
        }
        self.assertHttpBadRequest(self.api_client.post('/api/v1/register/', format='json', data=data))
       
    # check posting with no email 
    def test_post_no_email(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'firstname': 'demo',
            'lastname': 'user',
        }
        self.assertHttpBadRequest(self.api_client.post('/api/v1/register/', format='json', data=data))
     
    # check posting with invalid email
    def test_post_invalid_email(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'email': 'thisisnotanemailaddress',
            'passwordagain': 'secret',
            'firstname': 'demo',
            'lastname': 'user',
        }
        self.assertHttpBadRequest(self.api_client.post('/api/v1/register/', format='json', data=data))  
     
    # check posting with no passwordagain  
    def test_post_no_passwordagain(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'email': 'demo@demo.com',
            'firstname': 'demo',
            'lastname': 'user',
        }
        self.assertHttpBadRequest(self.api_client.post('/api/v1/register/', format='json', data=data)) 
        
    # test no firstname
    def test_post_no_firstname(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'lastname': 'user',
        }
        self.assertHttpBadRequest(self.api_client.post('/api/v1/register/', format='json', data=data))
        
    # test firstname long enough
    def test_post_firstname_length(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'firstname': 'd',
            'lastname': 'user',
        }
        self.assertHttpBadRequest(self.api_client.post('/api/v1/register/', format='json', data=data))
        
    # test no lastname
    def test_post_no_lastname(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'firstname': 'demo',
        }
        self.assertHttpBadRequest(self.api_client.post('/api/v1/register/', format='json', data=data))
        
    # test password long enough
    def test_post_password_length(self):
        data = {
            'username': 'demo2',
            'password': 's',
            'passwordagain': 's',
            'email': 'demo@demo.com',
            'firstname': 'demo',
            'lastname': 'user',
        }
        self.assertHttpBadRequest(self.api_client.post('/api/v1/register/', format='json', data=data))
    
    # test password and password again not matching
    def test_post_password_match(self):
        data = {
            'username': 'demo2',
            'password': 's',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'firstname': 'demo',
            'lastname': 'user',
        }
        self.assertHttpBadRequest(self.api_client.post('/api/v1/register/', format='json', data=data))
        
    # test lastname not long enough
    def test_post_lastname_length(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'firstname': 'demo',
            'lastname': 'u',
        }
        self.assertHttpBadRequest(self.api_client.post('/api/v1/register/', format='json', data=data))
    
    # test created (all data valid)
    def test_post_created(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'firstname': 'demo',
            'lastname': 'user',
        }
        self.assertHttpCreated(self.api_client.post('/api/v1/register/', format='json', data=data))

class ActivityScheduleResourceTest(ResourceTestCase):    
    def setUp(self):
        super(ActivityScheduleResourceTest, self).setUp()
      
    # check get not allowed
    def test_get_not_found(self):
        self.assertHttpNotFound(self.api_client.get('/api/v1/activityschedule', format='json')) 
        
    # check post not allowed
    def test_post_not_found(self):
        self.assertHttpNotFound(self.api_client.post('/api/v1/activityschedule', format='json', data={}))
        
# AwardsResource
class AwardsResourceTest(ResourceTestCase): 
    fixtures = ['user.json', 'oppia.json']   
    
    def setUp(self):
        super(AwardsResourceTest, self).setUp()
        user = User.objects.get(username='user')
        api_key = ApiKey.objects.get(user = user)
        self.auth_data = {
            'username': 'user',
            'api_key': api_key.key,
        }
        
    # check post not allowed
    def test_post_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.post('/api/v1/awards/', format='json', data={}))
        
    # check unauthorized
    def test_unauthorized(self):
        data = {
            'username': 'user',
            'api_key': '1234',
        }
        self.assertHttpUnauthorized(self.api_client.get('/api/v1/awards/', format='json', data=data))
    
    # check authorized
    def test_authorized(self):
        self.assertHttpOK(self.api_client.get('/api/v1/awards/', format='json', data=self.auth_data))
        
    # check returning a set of objects - expecting zero
    def test_no_objects(self):
        resp = self.api_client.get('/api/v1/awards/', format='json', data=self.auth_data)
        self.assertEqual(len(self.deserialize(resp)['objects']), 0)
        
    
# BadgesResource
# CourseResource
# CourseTagResource
# ModuleResource
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
# QuizAttemptResource

# signals tests

# cron/badges tests






