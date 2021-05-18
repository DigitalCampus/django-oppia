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

    user_all_feedback_user = reverse('profile:user_all_feedback_responses',
                                     args=[2])
    user_all_feedback_admin = reverse('profile:user_all_feedback_responses',
                                      args=[1])

    feedback_template = 'profile/quiz/attempts.html'

    def test_feedback_list_admin_get_user(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(self.user_all_feedback_user)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.feedback_template)

    def test_feedback_list_staff_get_user(self):
        self.client.force_login(user=self.staff_user)
        response = self.client.get(self.user_all_feedback_user)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.feedback_template)

    def test_feedback_list_teacher_get_user(self):
        self.client.force_login(user=self.teacher_user)
        response = self.client.get(self.user_all_feedback_user)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.feedback_template)

    def test_feedback_list_user_get_user(self):
        self.client.force_login(user=self.normal_user)
        response = self.client.get(self.user_all_feedback_user)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.feedback_template)

    def test_feedback_list_admin_get_admin(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(self.user_all_feedback_admin)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.feedback_template)

    def test_feedback_list_staff_get_admin(self):
        self.client.force_login(user=self.staff_user)
        response = self.client.get(self.user_all_feedback_admin)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.feedback_template)

    def test_feedback_list_teacher_get_admin(self):
        self.client.force_login(user=self.teacher_user)
        response = self.client.get(self.user_all_feedback_admin)
        self.assertEqual(403, response.status_code)
        self.assertTemplateUsed(self.feedback_template)

    def test_feedback_list_user_get_admin(self):
        self.client.force_login(user=self.normal_user)
        response = self.client.get(self.user_all_feedback_admin)
        self.assertEqual(403, response.status_code)
        self.assertTemplateUsed(self.feedback_template)
