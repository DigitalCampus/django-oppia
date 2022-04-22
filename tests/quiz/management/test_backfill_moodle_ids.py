import os
from io import StringIO

from django.conf import settings
from django.core.management import call_command

from oppia.test import OppiaTestCase

from quiz.models import Quiz, Question, QuizProps, QuestionProps


class BackfillMoodleIdsTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_customfields.json',
                'tests/test_oppia.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json',
                'tests/quiz/test_backfill_moodle_ids.json']

    def test_backfill(self):

        quiz_props_count_start = QuizProps.objects.all().count()
        question_props_count_start = QuestionProps.objects.all().count()

        out = StringIO()
        call_command('backfill_moodle_ids',
                     os.path.join(settings.FIXTURES_PATH, 'tests', 'quiz', 'module.xml'),
                     stdout=out)

        quiz_props_count_end = QuizProps.objects.all().count()
        question_props_count_end = QuestionProps.objects.all().count()

        # check correct no props added
        self.assertEqual(quiz_props_count_start+2, quiz_props_count_end)
        self.assertEqual(question_props_count_start+1,
                         question_props_count_end)

        # check value of props is correct
        quiz = Quiz.objects.get(
            quizprops__name="digest",
            quizprops__value="338898cb3afc9cfe734d19862cb0242a")
        quizprop = QuizProps.objects.get(quiz=quiz, name="moodle_quiz_id")
        self.assertEqual(int(quizprop.value), 7734)

        questionprop = QuestionProps.objects.get(question__pk=3,
                                                 name="moodle_question_id")
        self.assertEqual(int(questionprop.value), 9988)
