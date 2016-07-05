# oppia/tests/quiz/test_auiz_api.py
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from oppia.models import Tracker
from oppia.quiz.models import QuizAttempt,QuizAttemptResponse

from tastypie.models import ApiKey
from tastypie.test import ResourceTestCase

# QuizAttemptResource   
class QuizAttemptResourceTest(ResourceTestCase): 
    fixtures = ['user.json', 'oppia.json', 'quiz.json'] 
    
    def setUp(self):
        super(QuizAttemptResourceTest, self).setUp()
        self.username = 'demo'
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
                "quiz_id":2,
                "maxscore":30,
                "score":10,
                "attempt_date":"2012-12-18T15:35:12",
                "responses":[
                             {"question_id":"132",
                              "score":0,
                              "text":"true"},
                             {"question_id":"133",
                              "score":10,
                              "text":"true"},
                             {"question_id":"134",
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
