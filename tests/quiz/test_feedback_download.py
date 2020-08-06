# coding: utf-8

from django.urls import reverse

from oppia.test import OppiaTestCase

from reports.models import DashboardAccessLog
from tests.defaults import UNAUTHORISED_TEMPLATE


class FeedbackDownloadTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_feedback.json',
                'default_gamification_events.json']
    STR_EXPECTED_CONTENT_TYPE = 'application/vnd.ms-excel;charset=utf-8'
    STR_URL_TEMPLATE = 'quiz:feedback_results_download'

    valid_course_valid_feedback_url = reverse(STR_URL_TEMPLATE,
                                              args=[183, 65323])
    invalid_course_valid_feedback_url = reverse(STR_URL_TEMPLATE,
                                                args=[0, 65323])
    valid_course_invalid_feedback_url = reverse(STR_URL_TEMPLATE,
                                                args=[183, 0])
    invalid_course_invalid_feedback_url = reverse(STR_URL_TEMPLATE,
                                                  args=[0, 0])
    course_feedback_mismatch_url = reverse(STR_URL_TEMPLATE,
                                           args=[1, 65323])

    def test_admin_download(self):
        count_start = DashboardAccessLog.objects.all().count()
        self.client.force_login(self.admin_user)
        response = self.client.get(self.valid_course_valid_feedback_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.STR_EXPECTED_CONTENT_TYPE,
                         response['content-type'])
        count_end = DashboardAccessLog.objects.all().count()
        self.assertEqual(count_start+1, count_end)

    def test_staff_download(self):
        count_start = DashboardAccessLog.objects.all().count()
        self.client.force_login(self.staff_user)
        response = self.client.get(self.valid_course_valid_feedback_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.STR_EXPECTED_CONTENT_TYPE,
                         response['content-type'])
        count_end = DashboardAccessLog.objects.all().count()
        self.assertEqual(count_start+1, count_end)

    def test_teacher_download(self):
        count_start = DashboardAccessLog.objects.all().count()
        self.client.force_login(self.teacher_user)
        response = self.client.get(self.valid_course_valid_feedback_url)
        self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)
        self.assertEqual(403, response.status_code)
        count_end = DashboardAccessLog.objects.all().count()
        self.assertEqual(count_start, count_end)

    def test_user_download(self):
        count_start = DashboardAccessLog.objects.all().count()
        self.client.force_login(self.normal_user)
        response = self.client.get(self.valid_course_valid_feedback_url)
        self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)
        self.assertEqual(403, response.status_code)
        count_end = DashboardAccessLog.objects.all().count()
        self.assertEqual(count_start, count_end)

    def test_invalid_course_valid_feedback(self):
        users = [self.admin_user,
                 self.staff_user,
                 self.teacher_user,
                 self.normal_user]
        for user in users:
            count_start = DashboardAccessLog.objects.all().count()
            self.client.force_login(user)
            response = self.client.get(self.invalid_course_valid_feedback_url)
            self.assertEqual(404, response.status_code)
            count_end = DashboardAccessLog.objects.all().count()
            self.assertEqual(count_start, count_end)

    def test_valid_course_invalid_feedback(self):
        users = [self.admin_user,
                 self.staff_user,
                 self.teacher_user,
                 self.normal_user]
        for user in users:
            count_start = DashboardAccessLog.objects.all().count()
            self.client.force_login(user)
            response = self.client.get(self.valid_course_invalid_feedback_url)
            self.assertEqual(404, response.status_code)
            count_end = DashboardAccessLog.objects.all().count()
            self.assertEqual(count_start, count_end)

    def test_invalid_course_invalid_feedback(self):
        users = [self.admin_user,
                 self.staff_user,
                 self.teacher_user,
                 self.normal_user]
        for user in users:
            count_start = DashboardAccessLog.objects.all().count()
            self.client.force_login(user)
            response = self.client.get(
                self.invalid_course_invalid_feedback_url)
            self.assertEqual(404, response.status_code)
            count_end = DashboardAccessLog.objects.all().count()
            self.assertEqual(count_start, count_end)

    def test_course_feedback_mismatch(self):
        users = [self.admin_user,
                 self.staff_user,
                 self.teacher_user,
                 self.normal_user]
        for user in users:
            count_start = DashboardAccessLog.objects.all().count()
            self.client.force_login(user)
            response = self.client.get(self.course_feedback_mismatch_url)
            self.assertEqual(404, response.status_code)
            count_end = DashboardAccessLog.objects.all().count()
            self.assertEqual(count_start, count_end)
