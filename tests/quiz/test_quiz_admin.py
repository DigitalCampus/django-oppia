
from django.urls import reverse
from oppia.test import OppiaTestCase


class QuizAdminTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json',
                'tests/test_question_indices.json']

    def test_question_admin(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse('admin:quiz_question_changelist'))
        self.assertEqual(200, response.status_code)
