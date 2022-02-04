from io import StringIO

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
        call_command('backfill_moodle_ids', './oppia/fixtures/tests/quiz/module.xml', stdout=out)
        
        quiz_props_count_end = QuizProps.objects.all().count()
        question_props_count_end = QuestionProps.objects.all().count()
        
        self.assertEqual(quiz_props_count_start+6, quiz_props_count_end)
        self.assertEqual(question_props_count_start+1, question_props_count_end)
