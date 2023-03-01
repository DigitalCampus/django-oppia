import json

from django.contrib.auth.models import User

from tastypie.test import ResourceTestCaseMixin
from oppia.models import Activity, Section
from oppia.test import OppiaTestCase
from oppia.uploader import parse_and_save_quiz
from quiz.models import Quiz, QuizProps, QuestionProps
from tests.utils import get_api_key, get_api_url


class QuizUploadTestCase(ResourceTestCaseMixin, OppiaTestCase):

    def get_credentials(self):
        username = 'demo'
        user = User.objects.get(username=username)
        api_key = get_api_key(user).key
        return self.create_apikey(username, api_key)

    def upload(self, json_file, activity_type):
        user = User.objects.get(pk=1)
        with open(json_file) as json_data:
            quiz_contents = json_data.read()
            activity = self.create_activity(quiz_contents, activity_type)
            quiz_json = json.loads(quiz_contents)
            parse_and_save_quiz(user, activity)
            quiz_obj = Quiz.objects.get(pk=1)
            activity.save()
            return quiz_obj, quiz_json

    def create_activity(self, content, type):
        activity = Activity()
        activity.section = Section.objects.get(pk=1)
        activity.title = "Test activity"
        activity.description = "Test activity description"
        activity.type = type
        activity.order = 0
        activity.digest = '123'
        activity.content = content
        return activity

    def send_quiz_attempt(self, quiz_attempt_json_file):
        with open(quiz_attempt_json_file) as json_data:
            data = json.loads(json_data.read())
            resp = self.api_client.post(get_api_url('v2', 'quizattempt'),
                                        format='json',
                                        data=data,
                                        authentication=self.get_credentials())

            self.assertHttpCreated(resp)
            self.assertValidJSON(resp.content)

    def assert_quiz_props(self, quiz_obj, quiz_json):
        quiz_props = QuizProps.objects.filter(quiz=quiz_obj)
        for prop in quiz_props:
            self.assertEqual(str(quiz_json['props'][prop.name]), prop.value)

    def assert_question_props(self, question_obj, question_json):
        question_props = QuestionProps.objects.filter(question=question_obj)
        for prop in question_props:
            self.assertEqual(str(question_json['props'][prop.name]), prop.value)
