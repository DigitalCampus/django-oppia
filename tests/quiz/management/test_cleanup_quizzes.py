from io import StringIO
from django.core.management import call_command
from django.test import TestCase


class CleanUpQuizzesTest(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']

    def test_cleanup_quizzes(self):
        out = StringIO()
        call_command('cleanup_quizzes', stdout=out)
        contains_text = False
        if "No new elements to clean up." in out.getvalue():
            contains_text = True
        self.assertEqual(True, contains_text)