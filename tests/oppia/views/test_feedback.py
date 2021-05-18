
from django.urls import reverse

from oppia.test import OppiaTestCase


class FeedbackViewsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_cohort.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'tests/test_course_permissions.json',
                'tests/test_feedback.json']

    url_course_feedback = reverse('oppia:course_feedback', args=[1])
    url_course_feedback_response_list = reverse(
        'oppia:course_feedback_responses', args=[1, 65323])

    feedback_template = 'course/feedback.html'

    def test_feedback_list_get_admin(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(self.url_course_feedback)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.feedback_template)

    def test_feedback_list_get_staff(self):
        self.client.force_login(user=self.staff_user)
        response = self.client.get(self.url_course_feedback)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.feedback_template)

    def test_feedback_list_get_teacher(self):
        self.client.force_login(user=self.teacher_user)
        response = self.client.get(self.url_course_feedback)
        self.assertEqual(403, response.status_code)
        self.assertTemplateUsed(self.feedback_template)

    def test_feedback_list_get_user(self):
        self.client.force_login(user=self.normal_user)
        response = self.client.get(self.url_course_feedback)
        self.assertEqual(403, response.status_code)
        self.assertTemplateUsed(self.feedback_template)

    def test_feedback_response_list_get_admin(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(self.url_course_feedback_response_list)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.feedback_template)

    def test_feedback_response_list_get_staff(self):
        self.client.force_login(user=self.staff_user)
        response = self.client.get(self.url_course_feedback_response_list)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.feedback_template)

    def test_feedback_response_list_get_teacher(self):
        self.client.force_login(user=self.teacher_user)
        response = self.client.get(self.url_course_feedback_response_list)
        self.assertEqual(403, response.status_code)
        self.assertTemplateUsed(self.feedback_template)

    def test_feedback_response_list_get_user(self):
        self.client.force_login(user=self.normal_user)
        response = self.client.get(self.url_course_feedback_response_list)
        self.assertEqual(403, response.status_code)
        self.assertTemplateUsed(self.feedback_template)
