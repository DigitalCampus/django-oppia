# coding: utf-8

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TransactionTestCase
from tastypie.test import ResourceTestCaseMixin

from quiz.models import QuizAttemptResponse, QuizAttempt
from oppia.test import OppiaTestCase

from tests.defaults import UNAUTHORISED_TEMPLATE

from tests.utils import get_api_key, get_api_url


class FeedbackResourceTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_feedback.json',
                'default_gamification_events.json']
    valid_course_feedback_url = reverse('oppia:course_feedback_download',
                                        args=[183, 65323])

    def test_admin_download(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.valid_course_feedback_url)
        self.assertEqual(200, response.status_code)


    def test_staff_download(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(self.valid_course_feedback_url)
        self.assertEqual(200, response.status_code)

    def test_teacher_download(self):
        self.client.force_login(self.teacher_user)
        response = self.client.get(self.valid_course_feedback_url)
        self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)
        self.assertEqual(response.status_code, 403)

    def test_user_download(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(self.valid_course_feedback_url)
        self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)
        self.assertEqual(response.status_code, 403)