from django.urls import reverse
from oppia.test import OppiaTestCase


class OppiaAdminTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json',
                'tests/test_question_indices.json']

    def test_course_admin(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse('admin:oppia_course_changelist'))
        self.assertEqual(200, response.status_code)

    def test_activity_admin(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse('admin:oppia_activity_changelist'))
        self.assertEqual(200, response.status_code)
