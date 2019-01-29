from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from tests.utils import *

class UpdateShortAnswerScoresTest(TestCase):
    fixtures = ['tests/test_user.json', 
                'tests/test_oppia.json', 
                'tests/test_quiz.json', 
                'tests/test_permissions.json']
    
    quiz_file_path = './oppia/fixtures/reference_files/quiz_short_answer_update.cvs' 
    
    def setUp(self):
        super(UpdateShortAnswerScoresTest, self).setUp()