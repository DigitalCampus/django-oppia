from django.core.exceptions import PermissionDenied
from django.urls import reverse
from oppia.test import OppiaTestCase


class OppiaActivityViewsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_cohort.json']

    url_recent_activity = reverse('oppia_recent_activity', args=[1])
    url_recent_activity_detail = reverse('oppia_recent_activity_detail',
                                         args=[1])
    activity_detail_template = 'course/activity-detail.html'
    end_date = '2019-12-28 00:00:00'

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
               
    def test_recent_activity_post_dates(self):
        self.client.force_login(user=self.admin_user)
        post_data = {'start_date': '2019-11-28 00:00:00',
                     'end_date': self.end_date}
        response = self.client.post(self.url_recent_activity, data=post_data)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.activity_detail_template)

    def test_recent_activity_post_interval_days(self):
        self.client.force_login(user=self.admin_user)
        post_data = {'start_date': '2018-11-28 00:00:00',
                     'end_date': self.end_date,
                     'interval': 'days'}
        response = self.client.post(self.url_recent_activity, data=post_data)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.activity_detail_template)
    
    def test_recent_activity_post_interval_months(self):
        self.client.force_login(user=self.admin_user)
        post_data = {'start_date': '2018-11-28 00:00:00',
                     'end_date': self.end_date,
                     'interval': 'months'}
        response = self.client.post(self.url_recent_activity, data=post_data)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.activity_detail_template)

    def test_recent_activity_post_interval_other(self):
        self.client.force_login(user=self.admin_user)
        post_data = {'start_date': '2018-11-28 00:00:00',
                     'end_date': self.end_date,
                     'interval': 'something else'}
        response = self.client.post(self.url_recent_activity, data=post_data)
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
        response = self.client.get(self.url_recent_activity_detail)
        self.assertRaises(PermissionDenied)