from oppia.test import OppiaTestCase


class UpdateShortAnswerScoresTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']

    quiz_file_path = './oppia/fixtures/reference_files/quiz_short_answer_update.cvs'
