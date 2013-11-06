# oppia/tests.py
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from oppia.models import Tracker
from oppia.quiz.models import QuizAttempt,QuizAttemptResponse

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

    # TODO test login redirected correctly for all pages
    # except those with login exempt 
        
class RegisterResourceTest(ResourceTestCase):    
    fixtures = ['user.json']
    
    def setUp(self):
        super(RegisterResourceTest, self).setUp()
        self.url = '/api/v1/register/'
        
    # check get method not allowed  
    def test_get_list_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.get(self.url, format='json'))
    
    # check posting with no username
    def test_post_no_username(self):
        data = {
            'password': 'secret',
            'email': 'demo@demo.com',
            'passwordagain': 'secret',
            'firstname': 'demo',
            'lastname': 'user',
        }
        resp = self.api_client.post(self.url, format='json', data=data)
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
        resp = self.api_client.post(self.url, format='json', data=data)
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
        resp = self.api_client.post(self.url, format='json', data=data)
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
        resp = self.api_client.post(self.url, format='json', data=data)
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
        resp = self.api_client.post(self.url, format='json', data=data)
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
        resp = self.api_client.post(self.url, format='json', data=data)
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
        resp = self.api_client.post(self.url, format='json', data=data)
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
        resp = self.api_client.post(self.url, format='json', data=data)
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
        resp = self.api_client.post(self.url, format='json', data=data)
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
        resp = self.api_client.post(self.url, format='json', data=data)
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
        resp = self.api_client.post(self.url, format='json', data=data)
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
        resp = self.api_client.post(self.url, format='json', data=data)
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
        resp = self.api_client.post(self.url, format='json', data=data)
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
        resp = self.api_client.post(self.url, format='json', data=data)
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
        self.url = '/api/v1/awards/'
        
    # check post not allowed
    def test_post_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.post(self.url, format='json', data={}))
        
    # check unauthorized
    def test_unauthorized(self):
        data = {
            'username': 'user',
            'api_key': '1234',
        }
        self.assertHttpUnauthorized(self.api_client.get(self.url, format='json', data=data))
    
    # check authorized
    def test_authorized(self):
        resp = self.api_client.get(self.url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        
    # check returning a set of objects - expecting zero
    def test_no_objects(self):
        resp = self.api_client.get(self.url, format='json', data=self.auth_data)
        self.assertValidJSON(resp.content)
        self.assertEqual(len(self.deserialize(resp)['objects']), 0)
    
# TODO BadgesResource

# CourseResource
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
        # should have 2 courses with the test data set
        self.assertEquals(len(response_data['courses']),2)
        # check each course had a download url
        for course in response_data['courses']:
            self.assertTrue('url' in course)
            self.assertTrue('shortname' in course)
            self.assertTrue('title' in course)
            self.assertTrue('version' in course)
       
    # test course file found     
    def test_course_download_file_found(self):
        resp = self.api_client.get(self.url+"20/download/", format='json', data=self.auth_data)
        self.assertHttpOK(resp)
        
    # TODO course file not found
    def test_course_download_file_not_found(self):
        #resp = self.api_client.get(self.url+"9999/download/", data=self.auth_data)
        #self.assertHttpNotFound(resp)
        pass
    
# CourseTagResource
class CourseTagResourceTest(ResourceTestCase):    
    def setUp(self):
        super(CourseTagResourceTest, self).setUp()
        self.url = '/api/v1/coursetag/'
        
    # check get not allowed
    def test_get_not_found(self):
        self.assertHttpNotFound(self.api_client.get(self.url, format='json')) 
        
    # check post not allowed
    def test_post_not_found(self):
        self.assertHttpNotFound(self.api_client.post(self.url, format='json', data={}))
        
# TODO PointsResource
# TODO ScheduleResource
# TODO ScorecardResource

# TODO TagResource
class TagResourceTest(ResourceTestCase): 
    fixtures = ['user.json', 'oppia.json'] 
    
    def setUp(self):
        super(TagResourceTest, self).setUp()
        user = User.objects.get(username='user')
        api_key = ApiKey.objects.get(user = user)
        self.auth_data = {
            'username': 'user',
            'api_key': api_key.key,
        }
        self.url = '/api/v1/tag/'
        
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
    
    # test valid json response and with 5 tags
    def test_has_tags(self):
        resp = self.api_client.get(self.url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('tags' in response_data)
        # should have 5 tags with the test data set
        self.assertEquals(len(response_data['tags']),5)
        # check each course had a download url
        for tag in response_data['tags']:
            self.assertTrue('count' in tag)
            self.assertTrue('id' in tag)
            self.assertTrue('name' in tag)
            # check count not 0
            self.assertTrue(tag['count'] > 0 )
            # check name not null
            self.assertTrue(len(tag['name']) > 0 )
            
    # test getting a listing of courses for one of the tags
    def test_tag_list(self):
        resp = self.api_client.get(self.url+"11/", format='json', data=self.auth_data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('courses' in response_data)
        self.assertTrue('count' in response_data)
        self.assertTrue('name' in response_data)
        self.assertEqual(len(response_data['courses']),response_data['count'])
        for course in response_data['courses']:
            self.assertTrue('shortname' in course)
            self.assertTrue('title' in course)
            self.assertTrue('url' in course)
            self.assertTrue('version' in course)
        
    # test getting listing of courses for an invalid tag
    def test_tag_not_found(self):
        resp = self.api_client.get(self.url+"999/", format='json', data=self.auth_data)
        self.assertHttpNotFound(resp)
        
# TrackerResource
class TrackerResourceTest(ResourceTestCase): 
    fixtures = ['user.json', 'oppia.json']  
    
    def setUp(self):
        super(TrackerResourceTest, self).setUp()
        self.username = 'user'
        user = User.objects.get(username=self.username)
        api_key = ApiKey.objects.get(user = user)
        self.api_key = api_key.key
        self.url = '/api/v1/tracker/'
     
    def get_credentials(self):
        return self.create_apikey(username=self.username, api_key=self.api_key)
   
    # check get not allowed
    def test_get_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.get(self.url))
    
    # test unauthorized
    def test_unauthorized(self):
        data = {
            'digest': '123456789123456789',
        }
        bad_auth = self.create_apikey(username=self.username, api_key="1234")
        self.assertHttpUnauthorized(self.api_client.post(self.url, format='json', data=data, authentication=bad_auth))
         
    # check put not allowed
    def test_put_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.put(self.url+"1/"))
            
    # test what happens when the digest is not found
    # should still add the record
    def test_post_digest_not_found(self):
        data = {
            'digest': '123456789123456789',
        }
        tracker_count_start = Tracker.objects.all().count()
        resp = self.api_client.post(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)
        self.assertValidJSON(resp.content)
        
    # test when 
    def test_post_digest_found(self):
        data = {
            'digest': '18ec12e5653a40431f453cce35811fa4',
        }
        tracker_count_start = Tracker.objects.all().count()
        resp = self.api_client.post(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)
        # check the record was succesfully added
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)
        
        # check that all data is there
        response_data = self.deserialize(resp)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)
        self.assertTrue('completed' in response_data)
        self.assertFalse(response_data['completed'])
        
    # check existing trackers can't be overwritten
    def test_post_no_overwrite(self):
        data = {
            'digest': '18ec12e5653a40431f453cce35811fa4',
        }
        resp = self.api_client.post(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)
        
        data = {
            'digest': '18ec12e5653a40431f453cce35811fa4',
        }
        tracker_count_start = Tracker.objects.all().count()
        resp = self.api_client.post(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)
        
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)
        
        response_data = self.deserialize(resp)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)
        
    def test_patch_all_valid_digests(self):
        activity1 = {
            'digest': '18ec12e5653a40431f453cce35811fa4', #page
        }
        activity2 = {
            'digest': '3ec4d8ab03c3c6bd66b3805f0b11225b', #media
        }
        activity3 = {
            'digest': '74ff568f95ddcfeb4ac809012eea7b5e', #quiz
        }
        
        data = {'objects':[activity1,activity2,activity3]}
        tracker_count_start = Tracker.objects.all().count()
        resp = self.api_client.patch(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+3, tracker_count_end)
    
        response_data = self.deserialize(resp)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)
        
    def test_patch_all_invalid_digests(self):   
        activity1 = {
            'digest': 'a1b2c3d4e5f6a7b8c9d', #invalid
        }
        activity2 = {
            'digest': 'a1b2c3d4e5f6a7b8c9d', #invalid
        }
        activity3 = {
            'digest': 'a1b2c3d4e5f6a7b8c9d', #invalid
        }
        
        data = {'objects':[activity1,activity2,activity3]}
        tracker_count_start = Tracker.objects.all().count()
        resp = self.api_client.patch(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+3, tracker_count_end)
        
        response_data = self.deserialize(resp)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)
        
    def test_patch_mix_invalid_valid_digests(self):
        activity1 = {
            'digest': '18ec12e5653a40431f453cce35811fa4', #page
        }
        activity2 = {
            'digest': '3ec4d8ab03c3c6bd66b3805f0b11225b', #media
        }
        activity3 = {
            'digest': 'a1b2c3d4e5f6a7b8c9d', #quiz
        }
        
        data = {'objects':[activity1,activity2,activity3]}
        tracker_count_start = Tracker.objects.all().count()
        resp = self.api_client.patch(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+3, tracker_count_end)
        
        response_data = self.deserialize(resp)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)   
    
# UserResource
class UserResourceTest(ResourceTestCase): 
    fixtures = ['user.json', 'oppia.json']   
    
    def setUp(self):
        super(UserResourceTest, self).setUp()
        self.url = '/api/v1/user/'
        
    # check get not allowed
    def test_get_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.get(self.url, format='json'))
     
    # check valid login
    def test_valid_login(self):
        data = {
            'username': 'user',
            'password': 'demo'
        }
        resp = self.api_client.post(self.url, format='json', data=data)
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
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('error' in response_data) 
    
    # check no password
    def test_no_password(self):
        data = {
            'username': 'user',
        }
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('error' in response_data) 
    
    # check no username or password
    def test_no_username_password(self):
        data = {}
        resp = self.api_client.post(self.url, format='json', data=data)
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
        resp = self.api_client.post(self.url, format='json', data=data)
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('error' in response_data) 
    
    


# QuizAttemptResource   
class QuizAttemptResourceTest(ResourceTestCase): 
    fixtures = ['user.json', 'oppia.json', 'quiz.json'] 
    
    def setUp(self):
        super(QuizAttemptResourceTest, self).setUp()
        self.username = 'user'
        user = User.objects.get(username=self.username)
        api_key = ApiKey.objects.get(user = user)
        self.api_key = api_key.key
        self.url = '/api/v1/quizattempt/'
    
    def get_credentials(self):
        return self.create_apikey(username=self.username, api_key=self.api_key)
    
    # check get not allowed
    def test_get_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.get(self.url, format='json'))

    def test_put_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.put(self.url+"1192/", format='json'))
        
    def test_delete_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.delete(self.url+"1192/", format='json'))
    
    def test_authorized(self):
        data = {
                "quiz_id":"354",
                "maxscore":30,
                "score":10,
                "attempt_date":"2012-12-18T15:35:12",
                "responses":[
                             {"question_id":"1839",
                              "score":0,
                              "text":"true"},
                             {"question_id":"1840",
                              "score":10,
                              "text":"true"},
                             {"question_id":"1841",
                              "score":0,
                              "text":"false"}]}
        quizattempt_count_start = QuizAttempt.objects.all().count()
        quizattemptresponse_count_start = QuizAttemptResponse.objects.all().count()
        resp = self.api_client.post(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)
        
        quizattempt_count_end = QuizAttempt.objects.all().count()
        quizattemptresponse_count_end = QuizAttemptResponse.objects.all().count()
        self.assertEqual(quizattempt_count_start+1, quizattempt_count_end)
        self.assertEqual(quizattemptresponse_count_start+3, quizattemptresponse_count_end)
      
    def test_unauthorized(self):
        data = {
                "quiz_id":"354",
                "maxscore":30,
                "score":10,
                "attempt_date":"2012-12-18T15:35:12",
                "responses":[
                             {"question_id":"1839",
                              "score":0,
                              "text":"true"},
                             {"question_id":"1840",
                              "score":10,
                              "text":"true"},
                             {"question_id":"1841",
                              "score":0,
                              "text":"false"}]}
        bad_auth = self.create_apikey(username=self.username, api_key="1234")
        quizattempt_count_start = QuizAttempt.objects.all().count()
        quizattemptresponse_count_start = QuizAttemptResponse.objects.all().count()
        resp = self.api_client.post(self.url, format='json', data=data, authentication=bad_auth) 
        self.assertHttpUnauthorized(resp)
        
        quizattempt_count_end = QuizAttempt.objects.all().count()
        quizattemptresponse_count_end = QuizAttemptResponse.objects.all().count()
        self.assertEqual(quizattempt_count_start, quizattempt_count_end)
        self.assertEqual(quizattemptresponse_count_start, quizattemptresponse_count_end)
        
    def test_invalid_quiz_id(self):
        data = {
                "quiz_id":"100", # this quiz id doesn't exist in the test data
                "maxscore":30,
                "score":10,
                "attempt_date":"2012-12-18T15:35:12",
                "responses":[
                             {"question_id":"1839",
                              "score":0,
                              "text":"true"},
                             {"question_id":"1840",
                              "score":10,
                              "text":"true"},
                             {"question_id":"1841",
                              "score":0,
                              "text":"false"}]}
        quizattempt_count_start = QuizAttempt.objects.all().count()
        quizattemptresponse_count_start = QuizAttemptResponse.objects.all().count()
        resp = self.api_client.post(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        
        quizattempt_count_end = QuizAttempt.objects.all().count()
        quizattemptresponse_count_end = QuizAttemptResponse.objects.all().count()
        self.assertEqual(quizattempt_count_start, quizattempt_count_end)
        self.assertEqual(quizattemptresponse_count_start, quizattemptresponse_count_end)   
        
    def test_invalid_question_id(self):
        data = {
                "quiz_id":"354", 
                "maxscore":30,
                "score":10,
                "attempt_date":"2012-12-18T15:35:12",
                "responses":[
                             {"question_id":"1111", # this question id doesn't exist in the test data
                              "score":0,
                              "text":"true"},
                             {"question_id":"1840",
                              "score":10,
                              "text":"true"},
                             {"question_id":"1841",
                              "score":0,
                              "text":"false"}]}
        quizattempt_count_start = QuizAttempt.objects.all().count()
        quizattemptresponse_count_start = QuizAttemptResponse.objects.all().count()
        resp = self.api_client.post(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        
        quizattempt_count_end = QuizAttempt.objects.all().count()
        quizattemptresponse_count_end = QuizAttemptResponse.objects.all().count()
        self.assertEqual(quizattempt_count_start, quizattempt_count_end)
        self.assertEqual(quizattemptresponse_count_start, quizattemptresponse_count_end) 
        
    def test_question_is_part_of_quiz(self):
        data = {
                "quiz_id":"354", 
                "maxscore":30,
                "score":10,
                "attempt_date":"2012-12-18T15:35:12",
                "responses":[
                             {"question_id":"1884", # this question id is valid but not part of this quiz
                              "score":0,
                              "text":"true"},
                             {"question_id":"1840",
                              "score":10,
                              "text":"true"},
                             {"question_id":"1841",
                              "score":0,
                              "text":"false"}]}
        quizattempt_count_start = QuizAttempt.objects.all().count()
        quizattemptresponse_count_start = QuizAttemptResponse.objects.all().count()
        resp = self.api_client.post(self.url, format='json', data=data, authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)
        
        quizattempt_count_end = QuizAttempt.objects.all().count()
        quizattemptresponse_count_end = QuizAttemptResponse.objects.all().count()
        self.assertEqual(quizattempt_count_start, quizattempt_count_end)
        self.assertEqual(quizattemptresponse_count_start, quizattemptresponse_count_end) 
        
# TODO QuizQuestionResource
# TODO QuestionResource
# TODO QuestionPropsResource
# TODO ResponseResource
# TODO ResponsePropsResource
# TODO QuizPropsResource
    # getting a quiz via digest
    
# TODO QuizResource
    # TODO check get and post valid
    # getting a quiz via id no
    
    # getting an invalid digest
    # creating a quiz (and data required etc)


# TODO signals tests
    # TODO test points awarded for one day but not twice on same day for page
    # TODO test points awarded for one day but not twice on same day for quiz
    # TODO test points awarded for one day but not twice on same day for media
    
    
# TODO cron/badges tests






