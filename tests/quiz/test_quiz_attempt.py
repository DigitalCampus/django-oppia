# coding: utf-8

# QuizAttemptResource
from django.contrib.auth.models import User
from django.test import TransactionTestCase
from tastypie.test import ResourceTestCaseMixin

from quiz.models import QuizAttemptResponse, QuizAttempt
from tests.utils import get_api_key, get_api_url


class QuizAttemptResourceTest(ResourceTestCaseMixin, TransactionTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'default_gamification_events.json',
                'tests/test_course_permissions.json']

    username = 'demo'

    def setUp(self):
        super(QuizAttemptResourceTest, self).setUp()
        user = User.objects.get(username=self.username)
        api_key = get_api_key(user)
        self.api_key = api_key.key
        self.url = get_api_url('v2', 'quizattempt')

    def get_credentials(self):
        return self.create_apikey(username=self.username,
                                  api_key=self.api_key)

    # check get not allowed
    def test_get_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.get(self.url,
                                                            format='json'))

    def test_put_invalid(self):
        resource_url = get_api_url('v1', 'quizattempt', 1192)
        self.assertHttpMethodNotAllowed(self.api_client.put(resource_url,
                                                            format='json'))

    def test_delete_invalid(self):
        resource_url = get_api_url('v1', 'quizattempt', 1192)
        self.assertHttpMethodNotAllowed(self.api_client.delete(resource_url,
                                                               format='json'))

    def test_authorized(self):
        data = {
                "quiz_id": 2,
                "maxscore": 30,
                "score": 10,
                "attempt_date": "2012-12-18T15:35:12",
                "instance_id": "343c1dbf-b61a-4b74-990c-b94e3dc7d855",
                "responses": [
                             {"question_id": "132",
                              "score": 0,
                              "text": "true"},
                             {"question_id": "133",
                              "score": 10,
                              "text": "true"},
                             {"question_id": "134",
                              "score": 0,
                              "text": "false"}]}
        quizattempt_count_start = QuizAttempt.objects.all().count()
        quizattemptresponse_count_start = QuizAttemptResponse.objects \
            .all().count()
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=data,
                                    authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)

        quizattempt_count_end = QuizAttempt.objects.all().count()
        quizattemptresponse_count_end = QuizAttemptResponse.objects \
            .all().count()
        self.assertEqual(quizattempt_count_start + 1, quizattempt_count_end)
        self.assertEqual(quizattemptresponse_count_start + 3,
                         quizattemptresponse_count_end)

    def test_time_taken_saved(self):
        data = {
                "quiz_id": 2,
                "maxscore": 30,
                "score": 10,
                "attempt_date": "2012-12-18T15:35:12",
                "instance_id": "343c1dbf-b61a-4b74-990c-b94e3dc7d855",
                "responses": [
                             {"question_id": "132",
                              "score": 0,
                              "text": "true"},
                             {"question_id": "133",
                              "score": 10,
                              "text": "true"},
                             {"question_id": "134",
                              "score": 0,
                              "text": "false"}],
                "timetaken": 120}
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=data,
                                    authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)
        quiz_attempt = QuizAttempt.objects.latest('submitted_date')

        self.assertEqual(120, quiz_attempt.time_taken)

    def test_unauthorized(self):
        data = {
                "quiz_id": "354",
                "maxscore": 30,
                "score": 10,
                "attempt_date": "2012-12-18T15:35:12",
                "instance_id": "343c1dbf-b61a-4b74-990c-b94e3dc7d855",
                "responses": [
                             {"question_id": "1839",
                              "score": 0,
                              "text": "true"},
                             {"question_id": "1840",
                              "score": 10,
                              "text": "true"},
                             {"question_id": "1841",
                              "score": 0,
                              "text": "false"}]}
        bad_auth = self.create_apikey(username=self.username, api_key="1234")
        quizattempt_count_start = QuizAttempt.objects.all().count()
        quizattemptresponse_count_start = QuizAttemptResponse.objects \
            .all().count()
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=data,
                                    authentication=bad_auth)
        self.assertHttpUnauthorized(resp)

        quizattempt_count_end = QuizAttempt.objects.all().count()
        quizattemptresponse_count_end = QuizAttemptResponse.objects \
            .all().count()
        self.assertEqual(quizattempt_count_start, quizattempt_count_end)
        self.assertEqual(quizattemptresponse_count_start,
                         quizattemptresponse_count_end)

    def test_invalid_quiz_id(self):
        data = {
                # this quiz id doesn't exist in the test data
                "quiz_id": "100",
                "maxscore": 30,
                "score": 10,
                "attempt_date": "2012-12-18T15:35:12",
                "instance_id": "343c1dbf-b61a-4b74-990c-b94e3dc7d855",
                "responses": [
                             {"question_id": "1839",
                              "score": 0,
                              "text": "true"},
                             {"question_id": "1840",
                              "score": 10,
                              "text": "true"},
                             {"question_id": "1841",
                              "score": 0,
                              "text": "false"}]}
        quizattempt_count_start = QuizAttempt.objects.all().count()
        quizattemptresponse_count_start = QuizAttemptResponse.objects \
            .all().count()
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=data,
                                    authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

        quizattempt_count_end = QuizAttempt.objects.all().count()
        quizattemptresponse_count_end = QuizAttemptResponse.objects \
            .all().count()
        self.assertEqual(quizattempt_count_start, quizattempt_count_end)
        self.assertEqual(quizattemptresponse_count_start,
                         quizattemptresponse_count_end)

    def test_invalid_question_id(self):
        data = {
                "quiz_id": "354",
                "maxscore": 30,
                "score": 10,
                "attempt_date": "2012-12-18T15:35:12",
                "instance_id": "343c1dbf-b61a-4b74-990c-b94e3dc7d855",
                "responses": [
                             # this question id doesn't exist in the test data
                             {"question_id": "1111",
                              "score": 0,
                              "text": "true"},
                             {"question_id": "1840",
                              "score": 10,
                              "text": "true"},
                             {"question_id": "1841",
                              "score": 0,
                              "text": "false"}]}
        quizattempt_count_start = QuizAttempt.objects.all().count()
        quizattemptresponse_count_start = QuizAttemptResponse.objects \
            .all().count()
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=data,
                                    authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

        quizattempt_count_end = QuizAttempt.objects.all().count()
        quizattemptresponse_count_end = QuizAttemptResponse.objects \
            .all().count()
        self.assertEqual(quizattempt_count_start, quizattempt_count_end)
        self.assertEqual(quizattemptresponse_count_start,
                         quizattemptresponse_count_end)

    def test_question_is_part_of_quiz(self):
        data = {
                "quiz_id": "354",
                "maxscore": 30,
                "score": 10,
                "attempt_date": "2012-12-18T15:35:12",
                "instance_id": "343c1dbf-b61a-4b74-990c-b94e3dc7d855",
                "responses": [
                             # this question id is valid but not part of this
                             # quiz
                             {"question_id": "1884",
                              "score": 0,
                              "text": "true"},
                             {"question_id": "1840",
                              "score": 10,
                              "text": "true"},
                             {"question_id": "1841",
                              "score": 0,
                              "text": "false"}]}
        quizattempt_count_start = QuizAttempt.objects.all().count()
        quizattemptresponse_count_start = QuizAttemptResponse.objects \
            .all().count()
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=data,
                                    authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

        quizattempt_count_end = QuizAttempt.objects.all().count()
        quizattemptresponse_count_end = QuizAttemptResponse.objects \
            .all().count()
        self.assertEqual(quizattempt_count_start, quizattempt_count_end)
        self.assertEqual(quizattemptresponse_count_start,
                         quizattemptresponse_count_end)

    def test_duplicate_quiz_attempt(self):

        data = {
            "quiz_id": 2,
            "maxscore": 30,
            "score": 10,
            "attempt_date": "2012-12-18T15:35:12",
            "instance_id": "343c1dbf-b61a-4b74-990c-b94e3dc7d855",
            "responses": [
                         {"question_id": "132",
                          "score": 0,
                          "text": "true"},
                         {"question_id": "133",
                          "score": 10,
                          "text": "true"},
                         {"question_id": "134",
                          "score": 0,
                          "text": "false"}]}
        quizattempt_count_start = QuizAttempt.objects.all().count()
        quizattemptresponse_count_start = QuizAttemptResponse.objects \
            .all().count()
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=data,
                                    authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertValidJSON(resp.content)

        quizattempt_count_end = QuizAttempt.objects.all().count()
        quizattemptresponse_count_end = QuizAttemptResponse.objects \
            .all().count()
        self.assertEqual(quizattempt_count_start + 1,
                         quizattempt_count_end)
        self.assertEqual(quizattemptresponse_count_start + 3,
                         quizattemptresponse_count_end)

        # now send same data again
        quizattempt_count_start = QuizAttempt.objects.all().count()
        quizattemptresponse_count_start = QuizAttemptResponse.objects \
            .all().count()
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=data,
                                    authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

        quizattempt_count_end = QuizAttempt.objects.all().count()
        quizattemptresponse_count_end = QuizAttemptResponse.objects \
            .all().count()
        self.assertEqual(quizattempt_count_start, quizattempt_count_end)
        self.assertEqual(quizattemptresponse_count_start,
                         quizattemptresponse_count_end)
