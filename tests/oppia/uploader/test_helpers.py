import json
import os

from django.contrib.auth.models import User
from django.conf import settings
from oppia.test import OppiaTestCase

from oppia.uploader import create_or_update_quiz_props, create_quiz_questions
from quiz.models import Quiz, QuizProps, QuizQuestion


class UploadHelpersTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_badges.json',
                'tests/test_course_permissions.json']
    quiz_json_file = os.path.join(settings.TEST_RESOURCES, 'sample_quiz.json')

    def test_create_quiz_props(self):
        # get existing quiz and remove existing props
        quiz = Quiz.objects.get(pk=1)
        QuizProps.objects.filter(quiz=quiz).delete()

        with open(self.quiz_json_file) as json_data:
            quiz_obj = json.load(json_data)

        quiz_obj['id'] = quiz.pk

        create_or_update_quiz_props(quiz, quiz_obj)

        # now check the props have been saved correctly
        # (using the sample quiz file)
        quiz_prop_count = QuizProps.objects.filter(quiz=quiz).count()
        self.assertEqual(quiz_prop_count, 7)

        digest = QuizProps.objects.get(quiz=quiz, name='digest')
        self.assertEqual(digest.value,
                         "4d46a0566501cdbc1f57b2b505c92a2d17703cr0s2a1p80a0")

    def test_create_quiz_questions(self):
        quiz = Quiz.objects.get(pk=1)
        QuizQuestion.objects.filter(quiz=quiz).delete()

        # check no questions
        no_questions = QuizQuestion.objects.filter(quiz=quiz).count()
        self.assertEqual(no_questions, 0)

        with open(self.quiz_json_file) as json_data:
            quiz_obj = json.load(json_data)

        quiz_obj['id'] = quiz.pk

        user = User.objects.get(pk=1)
        create_quiz_questions(user, quiz, quiz_obj)

        # check no questions
        no_questions = QuizQuestion.objects.filter(quiz=quiz).count()
        self.assertEqual(no_questions, 10)
