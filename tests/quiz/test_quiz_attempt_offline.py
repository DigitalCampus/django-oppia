# coding: utf-8
from django.contrib.auth.models import User
from django.test import TransactionTestCase
from tastypie.test import ResourceTestCaseMixin

from oppia.models import Points
from quiz.models import QuizAttemptResponse, QuizAttempt
from tests.utils import get_api_key, get_api_url


class QuizAttemptResourceTest(ResourceTestCaseMixin, TransactionTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'default_gamification_events.json',
                'tests/test_course_permissions.json']

    username = 'demo'
    url = get_api_url('v2', 'quizattempt')

    def get_credentials(self):
        user = User.objects.get(username=self.username)
        api_key = get_api_key(user)
        return self.create_apikey(username=self.username,
                                  api_key=api_key.key)

    def test_quiz_attempt_points_included(self):

        data = {
                "quiz_id": 2,
                "maxscore": 30,
                "score": 10,
                "attempt_date": "2012-12-18T15:35:12",
                "instance_id": "343c1dbf-b61a-4b74-990c-b94e3dc7d855",
                "points": 54,
                "event": "quiz_attempt",
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
        points_count_start = Points.objects.all().count()

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

        # check that the points info has not been added, else the points get
        # counted twice
        points_count_end = Points.objects.all().count()
        self.assertEqual(points_count_start, points_count_end)

        latest_points = Points.objects.get(pk=1)

        self.assertEqual(100, latest_points.points)
        self.assertEqual('signup', latest_points.type)

        # check that all data is there
        response_data = self.deserialize(resp)
        self.assertTrue('points' in response_data)
        self.assertTrue('badges' in response_data)
