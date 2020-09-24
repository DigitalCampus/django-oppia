
from django.core.exceptions import PermissionDenied
from django.core.paginator import InvalidPage
from django.forms import ValidationError
from django.urls import reverse
from oppia.test import OppiaTestCase


class OppiaActivityViewsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_cohort.json',
                'default_gamification_events.json',
                'tests/test_tracker.json',
                'tests/test_course_permissions.json']

    url_recent_activity = reverse('oppia:recent_activity', args=[1])
    url_recent_activity_detail = reverse('oppia:recent_activity_detail',
                                         args=[1])
    url_oppia_export_course_trackers = reverse('oppia:export_course_trackers',
                                               args=[1])

    activity_detail_template = 'course/activity-detail.html'
    start_date = '2018-11-28 00:00:00'
    end_date = '2019-12-28 00:00:00'
    interval_days = 'days'
    interval_months = 'months'
    interval_invalid = 'something'

    def test_recent_activity_get_admin(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(self.url_recent_activity)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.activity_detail_template)

    def test_recent_activity_get_staff(self):
        self.client.force_login(user=self.staff_user)
        response = self.client.get(self.url_recent_activity)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.activity_detail_template)

    def test_recent_activity_get_teacher(self):
        self.client.force_login(user=self.teacher_user)
        response = self.client.get(self.url_recent_activity)
        self.assertEqual(403, response.status_code)
        self.assertTemplateUsed(self.activity_detail_template)

    def test_recent_activity_get_user(self):
        self.client.force_login(user=self.normal_user)
        response = self.client.get(self.url_recent_activity)
        self.assertEqual(403, response.status_code)
        self.assertTemplateUsed(self.activity_detail_template)

    def test_recent_activity_invalid_course(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse('oppia:recent_activity',
                                           args=[999]))
        self.assertEqual(404, response.status_code)

    def test_recent_activity_post_dates(self):
        self.client.force_login(user=self.admin_user)
        post_data = {'start_date': self.start_date,
                     'end_date': self.end_date}
        response = self.client.post(self.url_recent_activity, data=post_data)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.activity_detail_template)

    def test_recent_activity_post_interval_days(self):
        self.client.force_login(user=self.admin_user)
        post_data = {'start_date': self.start_date,
                     'end_date': self.end_date,
                     'interval': self.interval_days}
        response = self.client.post(self.url_recent_activity, data=post_data)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.activity_detail_template)

    def test_recent_activity_post_interval_months(self):
        self.client.force_login(user=self.admin_user)
        post_data = {'start_date': self.start_date,
                     'end_date': self.end_date,
                     'interval': self.interval_months}
        response = self.client.post(self.url_recent_activity, data=post_data)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.activity_detail_template)

    def test_recent_activity_post_interval_other(self):
        self.client.force_login(user=self.admin_user)
        post_data = {'start_date': self.start_date,
                     'end_date': self.end_date,
                     'interval': self.interval_invalid}
        response = self.client.post(self.url_recent_activity, data=post_data)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.activity_detail_template)

    def test_recent_activity_post_invalid_dates(self):
        self.client.force_login(user=self.admin_user)
        post_data = {'start_date': '2020-12-28 00:00:00',
                     'end_date': '20-14-14 00:00:00',
                     'interval': self.interval_invalid}
        response = self.client.post(self.url_recent_activity, data=post_data)
        self.assertRaises(ValidationError)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.activity_detail_template)

    def test_recent_activity_detail_get_admin(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(self.url_recent_activity_detail)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.activity_detail_template)

    def test_recent_activity_detail_get_staff(self):
        self.client.force_login(user=self.staff_user)
        response = self.client.get(self.url_recent_activity_detail)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.activity_detail_template)

    def test_recent_activity_detail_get_teacher(self):
        self.client.force_login(user=self.teacher_user)
        self.client.get(self.url_recent_activity_detail)
        self.assertRaises(PermissionDenied)

    def test_recent_activity_detail_get_user(self):
        self.client.force_login(user=self.normal_user)
        self.client.get(self.url_recent_activity_detail)
        self.assertRaises(PermissionDenied)

    def test_recent_activity_detail_post_dates(self):
        self.client.force_login(user=self.admin_user)
        post_data = {'start_date': self.start_date,
                     'end_date': self.end_date}
        response = self.client.post(self.url_recent_activity_detail,
                                    data=post_data)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.activity_detail_template)

    def test_recent_activity_detail_post_invalid_dates(self):
        self.client.force_login(user=self.admin_user)
        post_data = {'start_date': '2020-12-28 00:00:00',
                     'end_date': '20-14-14 00:00:00',
                     'interval': 'days'}
        response = self.client.post(self.url_recent_activity_detail,
                                    data=post_data)
        self.assertRaises(ValidationError)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.activity_detail_template)

    def test_recent_activity_detail_get_page_1(self):
        self.client.force_login(user=self.admin_user)
        url = '%s?page=1' % self.url_recent_activity_detail
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.activity_detail_template)

    def test_recent_activity_detail_get_page_9999(self):
        self.client.force_login(user=self.admin_user)
        url = '%s?page=9999' % self.url_recent_activity_detail
        response = self.client.get(url)
        self.assertRaises(InvalidPage)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.activity_detail_template)

    def test_recent_activity_detail_get_page_abc(self):
        self.client.force_login(user=self.admin_user)
        url = '%s?page=abc' % self.url_recent_activity_detail
        response = self.client.get(url)
        self.assertRaises(ValueError)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.activity_detail_template)

    def test_export_course_trackers_admin(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(self.url_oppia_export_course_trackers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response['Content-Type'],
                         "application/vnd.ms-excel;charset=utf-8")

    def test_export_course_trackers_staff(self):
        self.client.force_login(user=self.staff_user)
        response = self.client.get(self.url_oppia_export_course_trackers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response['Content-Type'],
                         "application/vnd.ms-excel;charset=utf-8")

    def test_export_course_trackers_teacher(self):
        self.client.force_login(user=self.teacher_user)
        self.client.get(self.url_oppia_export_course_trackers)
        self.assertRaises(PermissionDenied)

    def test_export_course_trackers_user(self):
        self.client.force_login(user=self.normal_user)
        self.client.get(self.url_oppia_export_course_trackers)
        self.assertRaises(PermissionDenied)
