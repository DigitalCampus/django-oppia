from oppia.test import OppiaTestCase
from quiz.models import Question


class QuestionIndicesTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_question_indices.json',
                'tests/test_course_permissions.json']

    def test_question_number_responses(self):
        question = Question.objects.get(pk=21986)
        self.assertEqual(85, question.get_no_responses())

    def test_question_diff_index(self):
        question = Question.objects.get(pk=21986)
        self.assertAlmostEqual(0.576, question.get_difficulty_index(), 3)

    def test_question_disc_index(self):
        question = Question.objects.get(pk=21986)
        self.assertAlmostEqual(100, question.get_discrimination_index(), 1)
