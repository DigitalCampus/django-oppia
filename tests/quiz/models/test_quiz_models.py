from oppia.test import OppiaTestCase
from quiz.models import Quiz, QuizAttempt, Question, QuestionProps


class QuizModelsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'tests/test_quizattempt.json',
                'tests/test_course_permissions.json']

    '''
    Quiz model
    '''
    def test_quiz_avg_score_with_attempts(self):
        quiz = Quiz.objects.get(pk=2)
        self.assertEqual(23, quiz.avg_score())

    def test_quiz_avg_score_no_attempts(self):
        quiz = Quiz.objects.get(pk=1)
        self.assertEqual(0, quiz.avg_score())

    def test_quiz_is_baseline(self):
        quiz = Quiz.objects.get(pk=1)
        self.assertEqual(True, quiz.is_baseline())

    def test_quiz_not_baseline(self):
        quiz = Quiz.objects.get(pk=2)
        self.assertEqual(False, quiz.is_baseline())

    '''
    QuizAttempt model
    '''
    def test_quiz_attempt_first(self):
        quiz_attempt = QuizAttempt.objects.get(pk=140106)
        self.assertFalse(quiz_attempt.is_first_attempt())

    def test_quiz_attempt_digest(self):
        quiz_attempt = QuizAttempt.objects.get(pk=140106)
        self.assertEqual("d95762029b6285dae57385341145c40112153cr0s2a1p80a0",
                         quiz_attempt.get_quiz_digest())

    '''
    Question model
    '''
    def test_question_maxscore(self):
        question = Question.objects.get(pk=135)
        self.assertEqual(1, question.get_maxscore())

    def test_question_number_responses(self):
        question = Question.objects.get(pk=135)
        self.assertEqual(5, question.get_no_responses())

    def test_question_number_responses_none(self):
        question = Question.objects.get(pk=1)
        self.assertEqual(0, question.get_no_responses())

    def test_question_diff_index(self):
        question = Question.objects.get(pk=135)
        # will be 0 as not enough responses
        self.assertEqual(0, question.get_difficulty_index())

    def test_question_disc_index(self):
        question = Question.objects.get(pk=135)
        # will be 0 as not enough responses
        self.assertEqual(0, question.get_discrimination_index())

    def test_question_diff_index_no_responses(self):
        question = Question.objects.get(pk=1)
        self.assertEqual(0, question.get_difficulty_index())

    def test_question_disc_index_no_responses(self):
        question = Question.objects.get(pk=1)
        # will be 0 as not enough responses
        self.assertEqual(0, question.get_discrimination_index())

    '''
    QuestionProps Model
    '''
    def test_questionprops_name(self):
        question = Question.objects.get(pk=135)
        qp = QuestionProps.objects.get(question=question, name='maxscore')
        self.assertEqual("maxscore", str(qp))
