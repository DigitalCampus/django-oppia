import json

from django.contrib.auth.models import User
from django.test import TransactionTestCase
from tastypie.test import ResourceTestCaseMixin

from datarecovery.models import DataRecovery
from quiz.models import QuizAttemptResponse
from tests.utils import get_api_key, get_api_url


class DataRecoveryQuizTest(ResourceTestCaseMixin, TransactionTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json']

    username = 'demo'

    def setUp(self):
        super(DataRecoveryQuizTest, self).setUp()
        user = User.objects.get(username=self.username)
        api_key = get_api_key(user)
        self.api_key = api_key.key
        self.url = get_api_url('v2', 'quizattempt')

    def get_credentials(self):
        return self.create_apikey(username=self.username,
                                  api_key=self.api_key)

    def test_quiz_does_not_exist(self):
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
        datarecovery_count_start = DataRecovery.objects.all().count()
        quizattemptresponse_count_start = QuizAttemptResponse.objects.all().count()
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=data,
                                    authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

        datarecovery_count_end = DataRecovery.objects.all().count()
        quizattemptresponse_count_end = QuizAttemptResponse.objects.all().count()
        self.assertEqual(datarecovery_count_start + 1, datarecovery_count_end)
        self.assertEqual(quizattemptresponse_count_start, quizattemptresponse_count_end)

        # Assert Data Recovery object data
        datarecovery_obj = DataRecovery.objects.last()
        self.assertEqual(DataRecovery.Type.QUIZ, datarecovery_obj.data_type)
        self.assertEqual(DataRecovery.Reason.QUIZ_DOES_NOT_EXIST, datarecovery_obj.reasons)
        self.assertEqual(data, json.loads(datarecovery_obj.data))

    def test_question_does_not_exist(self):
        data = {
                "quiz_id": "1",
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
        datarecovery_count_start = DataRecovery.objects.all().count()
        quizattemptresponse_count_start = QuizAttemptResponse.objects \
            .all().count()
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=data,
                                    authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

        datarecovery_count_end = DataRecovery.objects.all().count()
        quizattemptresponse_count_end = QuizAttemptResponse.objects.all().count()
        self.assertEqual(datarecovery_count_start + 1, datarecovery_count_end)
        self.assertEqual(quizattemptresponse_count_start, quizattemptresponse_count_end)

        # Assert Data Recovery object data
        datarecovery_obj = DataRecovery.objects.last()
        self.assertEqual(DataRecovery.Type.QUIZ, datarecovery_obj.data_type)
        self.assertEqual(DataRecovery.Reason.QUESTION_DOES_NOT_EXIST, datarecovery_obj.reasons)
        self.assertEqual(data, json.loads(datarecovery_obj.data))

    def test_question_from_different_quiz(self):
        data = {
                "quiz_id": "1",
                "maxscore": 30,
                "score": 10,
                "attempt_date": "2012-12-18T15:35:12",
                "instance_id": "343c1dbf-b61a-4b74-990c-b94e3dc7d855",
                "responses": [
                             # this question id is valid but not part of this
                             # quiz
                             {"question_id": "218",
                              "score": 0,
                              "text": "true"},
                             {"question_id": "1840",
                              "score": 10,
                              "text": "true"},
                             {"question_id": "1841",
                              "score": 0,
                              "text": "false"}]}
        datarecovery_count_start = DataRecovery.objects.all().count()
        quizattemptresponse_count_start = QuizAttemptResponse.objects \
            .all().count()
        resp = self.api_client.post(self.url,
                                    format='json',
                                    data=data,
                                    authentication=self.get_credentials())
        self.assertHttpBadRequest(resp)
        self.assertValidJSON(resp.content)

        datarecovery_count_end = DataRecovery.objects.all().count()
        quizattemptresponse_count_end = QuizAttemptResponse.objects.all().count()
        self.assertEqual(datarecovery_count_start + 1, datarecovery_count_end)
        self.assertEqual(quizattemptresponse_count_start, quizattemptresponse_count_end)

        # Assert Data Recovery object data
        datarecovery_obj = DataRecovery.objects.last()
        self.assertEqual(DataRecovery.Type.QUIZ, datarecovery_obj.data_type)
        self.assertEqual(DataRecovery.Reason.QUESTION_FROM_DIFFERENT_QUIZ, datarecovery_obj.reasons)
        self.assertEqual(data, json.loads(datarecovery_obj.data))
