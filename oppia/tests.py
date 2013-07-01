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
    fixtures = ['user.json']
    
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
        resp = self.api_client.post('/api/v1/register/', format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
    
    # check posting with no password
    def test_post_no_password(self):
        data = {
            'username': 'demo2',
            'email': 'demo@demo.com',
            'passwordagain': 'secret',
            'firstname': 'demo',
            'lastname': 'user',
        }
        resp = self.api_client.post('/api/v1/register/', format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
       
    # check posting with no email 
    def test_post_no_email(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'firstname': 'demo',
            'lastname': 'user',
        }
        resp = self.api_client.post('/api/v1/register/', format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
     
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
        resp = self.api_client.post('/api/v1/register/', format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content) 
     
    # check posting with no passwordagain  
    def test_post_no_passwordagain(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'email': 'demo@demo.com',
            'firstname': 'demo',
            'lastname': 'user',
        }
        resp = self.api_client.post('/api/v1/register/', format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        
    # test no firstname
    def test_post_no_firstname(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'lastname': 'user',
        }
        resp = self.api_client.post('/api/v1/register/', format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        
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
        resp = self.api_client.post('/api/v1/register/', format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        
    # test no lastname
    def test_post_no_lastname(self):
        data = {
            'username': 'demo2',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'firstname': 'demo',
        }
        resp = self.api_client.post('/api/v1/register/', format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        
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
        resp = self.api_client.post('/api/v1/register/', format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
    
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
        resp = self.api_client.post('/api/v1/register/', format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        
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
        resp = self.api_client.post('/api/v1/register/', format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
    
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
        resp = self.api_client.post('/api/v1/register/', format='json', data=data)
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)
        
    # test username already in use
    def test_username_in_use(self):
        data = {
            'username': 'user',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'demo@demo.com',
            'firstname': 'demo',
            'lastname': 'user',
        }
        resp = self.api_client.post('/api/v1/register/', format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        
    # test email address already in use
    def test_email_in_use(self):
        data = {
            'username': 'demo3',
            'password': 'secret',
            'passwordagain': 'secret',
            'email': 'user@demo.com',
            'firstname': 'demo',
            'lastname': 'user',
        }
        resp = self.api_client.post('/api/v1/register/', format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
    
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
        resp = self.api_client.get('/api/v1/awards/', format='json', data=self.auth_data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        
    # check returning a set of objects - expecting zero
    def test_no_objects(self):
        resp = self.api_client.get('/api/v1/awards/', format='json', data=self.auth_data)
        self.assertValidJSON(resp.content)
        self.assertEqual(len(self.deserialize(resp)['objects']), 0)
    
# TODO BadgesResource

# TODO CourseResource
class CourseResourceTest(ResourceTestCase): 
    fixtures = ['user.json', 'oppia.json'] 
    
    def setUp(self):
        super(CourseResourceTest, self).setUp()
        user = User.objects.get(username='user')
        api_key = ApiKey.objects.get(user = user)
        self.auth_data = {
            'username': 'user',
            'api_key': api_key.key,
        }
        self.url = '/api/v1/course/'
        
    # Post invalid
    def test_post_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.post(self.url, format='json', data={}))
    
    # test unauthorized
    def test_unauthorized(self):
        data = {
            'username': 'user',
            'api_key': '1234',
        }
        self.assertHttpUnauthorized(self.api_client.get(self.url, format='json', data=data))
    
    # test authorized
    def test_authorized(self):
        resp = self.api_client.get(self.url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)
       
    # test contains courses (and right no of courses) 
    def test_has_courses(self):
        resp = self.api_client.get(self.url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('courses' in response_data)
        # should ahve 2 courses with the data set
        self.assertEquals(len(response_data['courses']),2)
        # check each course had a download url
        for course in response_data['courses']:
            self.assertTrue('url' in response_data)
       
    # TODO     
    def test_course_download_file_found(self):
        pass
    
    # TODO
    def test_course_download_file_not_found(self):
        pass
    
# CourseTagResource
class CourseTagResourceTest(ResourceTestCase):    
    def setUp(self):
        super(CourseTagResourceTest, self).setUp()
      
    # check get not allowed
    def test_get_not_found(self):
        self.assertHttpNotFound(self.api_client.get('/api/v1/coursetag/', format='json')) 
        
    # check post not allowed
    def test_post_not_found(self):
        self.assertHttpNotFound(self.api_client.post('/api/v1/coursetag/', format='json', data={}))
        
# TODO ModuleResource
# TODO PointsResource
# TODO ScheduleResource
# TODO ScorecardResource
# TODO TagResource
# TODO TrackerResource

# UserResource
class UserResourceTest(ResourceTestCase): 
    fixtures = ['user.json', 'oppia.json']   
    
    def setUp(self):
        super(UserResourceTest, self).setUp()
        
    # check get not allowed
    def test_get_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.get('/api/v1/user/', format='json'))
     
    # check valid login
    def test_valid_login(self):
        data = {
            'username': 'user',
            'password': 'demo'
        }
        resp = self.api_client.post('/api/v1/user/', format='json', data=data)
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)
        
        # check return data
        response_data = self.deserialize(resp)
        self.assertTrue('api_key' in response_data)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)            
        # check it doesn't contain the password
        self.assertFalse('password' in response_data)
        
    # check no username
    def test_no_username(self):
        data = {
            'password': 'demo'
        }
        resp = self.api_client.post('/api/v1/user/', format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('error' in response_data) 
    
    # check no password
    def test_no_password(self):
        data = {
            'username': 'user',
        }
        resp = self.api_client.post('/api/v1/user/', format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('error' in response_data) 
    
    # check no username or password
    def test_no_username_password(self):
        data = {}
        resp = self.api_client.post('/api/v1/user/', format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('error' in response_data) 
    
    # check invalid password
    def test_invalid_password(self):
        data = {
            'username': 'user',
            'password': 'demo123'
        }
        resp = self.api_client.post('/api/v1/user/', format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('error' in response_data) 
    
    

# TODO QuizResource
# TODO QuizQuestionResource
# TODO QuestionResource
# TODO QuestionPropsResource
# TODO ResponseResource
# TODO ResponsePropsResource
# TODO QuizPropsResource
# TODO QuizAttemptResource

# TODO signals tests

# TODO cron/badges tests






