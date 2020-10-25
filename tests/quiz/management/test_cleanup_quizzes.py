from io import StringIO

from django.core.management import call_command

from oppia.test import OppiaTestCase

from quiz.models import Quiz, QuizQuestion

class CleanUpQuizzesTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json',
                'tests/test_question_indices.json',
                'tests/test_quiz_cleanup.json']

    def test_cleanup_quizzes(self):
        
        start_no_quizzes = Quiz.objects.all().count()
        start_no_questions = QuizQuestion.objects.all().count()
        
        out = StringIO()
        call_command('cleanup_quizzes', stdout=out)
        
        end_no_quizzes = Quiz.objects.all().count()
        end_no_questions = QuizQuestion.objects.all().count()
        
        self.assertEqual(start_no_quizzes-5, end_no_quizzes)
        self.assertEqual(start_no_questions-4, end_no_questions)
