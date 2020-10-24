from io import StringIO
from django.core.management import call_command
from oppia.test import OppiaTransactionTestCase


class QuestionDifficultyTest(OppiaTransactionTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json',
                'tests/test_question_indices.json',]
    
    def test_invalid_quiz(self):
        out = StringIO()
        call_command('question_analysis', '1234', stdout=out)
        
    def test_valid_quiz(self):
        out = StringIO()
        call_command('question_analysis',
                     'dd677c7ce6ce8bebaed56dcd0ea0b4e715714cr10s2a0p80a0',
                     stdout=out)
        
    # question with not enough responses and show course title
    def test_not_enough_responses_quiz(self):
        out = StringIO()
        call_command('question_analysis',
                     '1234q0m0',
                     stdout=out)
    # difficulty index too easy
    
    # discrimination index below 40 - not useful
    
    
    
    