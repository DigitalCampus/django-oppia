import os
import shutil

import pytest

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TransactionTestCase
from tastypie.test import ResourceTestCaseMixin

from oppia.models import Tracker

from tests.utils import get_api_key, get_api_url


class DraftCourseAccessTest(ResourceTestCaseMixin, TransactionTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']

    STR_DOWNLOAD = 'download/'
    STR_ZIP_EXPECTED_CONTENT_TYPE = 'application/zip'
    TEST_COURSES = ['anc_test_course.zip', 'draft-20150611100319.zip']

    def setUp(self):
        super(DraftCourseAccessTest, self).setUp()
        self.user = User.objects.get(username='demo')
        self.admin = User.objects.get(username='admin')
        self.staff = User.objects.get(username='staff')
        self.teacher = User.objects.get(username='teacher')
        self.manager = User.objects.get(username='manager')
        self.viewer = User.objects.get(username='viewer')
        self.user_auth = {
            'username': 'demo',
            'api_key': get_api_key(user=self.user).key,
        }
        self.admin_auth = {
            'username': 'admin',
            'api_key': get_api_key(user=self.admin).key
        }
        self.staff_auth = {
            'username': 'staff',
            'api_key': get_api_key(user=self.staff).key
        }
        self.teacher_auth = {
            'username': 'teacher',
            'api_key': get_api_key(user=self.teacher).key
        }
        self.manager_auth = {
            'username': 'manager',
            'api_key': get_api_key(user=self.manager).key
        }
        self.viewer_auth = {
            'username': 'viewer',
            'api_key': get_api_key(user=self.viewer).key
        }
        self.live_course_url_pk = get_api_url('v2', 'course', 1) \
            + self.STR_DOWNLOAD
        self.draft_course_url_pk = get_api_url('v2', 'course', 3) \
            + self.STR_DOWNLOAD
        self.live_course_url_shortname = get_api_url('v2',
                                                     'course',
                                                     'anc1-all') \
            + self.STR_DOWNLOAD
        self.draft_course_url_shortname = get_api_url('v2',
                                                      'course',
                                                      'draft-test') \
            + self.STR_DOWNLOAD
        self.tag_url = get_api_url('v2', 'tag')
        self.draft_tag_url = get_api_url('v2', 'tag', 8)
        self.live_tag_url = get_api_url('v2', 'tag', 1)

        self.copy_test_courses()

    # Copy test courses to upload directory
    def copy_test_courses(self):
        for test_course in self.TEST_COURSES:
            src = os.path.join(settings.TEST_RESOURCES, test_course)
            dst = os.path.join(settings.COURSE_UPLOAD_DIR, test_course)
            shutil.copyfile(src, dst)

    # check the tag listings
    def test_admin_tags(self):
        resp = self.api_client.get(
            self.tag_url, format='json', data=self.admin_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('tags' in response_data)
        self.assertEqual(6, len(response_data['tags']))

    def test_staff_tags(self):
        resp = self.api_client.get(
            self.tag_url, format='json', data=self.staff_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('tags' in response_data)
        self.assertEqual(6, len(response_data['tags']))

    def test_teacher_tags(self):
        resp = self.api_client.get(
            self.tag_url, format='json', data=self.teacher_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('tags' in response_data)
        self.assertEqual(5, len(response_data['tags']))

    def test_user_tags(self):
        resp = self.api_client.get(
            self.tag_url, format='json', data=self.user_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('tags' in response_data)
        self.assertEqual(5, len(response_data['tags']))

    def test_manager_tags(self):
        resp = self.api_client.get(
            self.tag_url, format='json', data=self.manager_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('tags' in response_data)
        self.assertEqual(6, len(response_data['tags']))

    def test_viewer_tags(self):
        resp = self.api_client.get(
            self.tag_url, format='json', data=self.viewer_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('tags' in response_data)
        self.assertEqual(6, len(response_data['tags']))

    # check tag detail - draft
    def test_admin_draft_tag_detail(self):
        resp = self.api_client.get(
            self.draft_tag_url, format='json', data=self.admin_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('courses' in response_data)
        self.assertEqual(1, len(response_data['courses']))

    def test_staff_draft_tag_detail(self):
        resp = self.api_client.get(
            self.draft_tag_url, format='json', data=self.staff_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('courses' in response_data)
        self.assertEqual(1, len(response_data['courses']))

    def test_teacher_draft_tag_detail(self):
        resp = self.api_client.get(
            self.draft_tag_url, format='json', data=self.teacher_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('courses' in response_data)
        self.assertEqual(0, len(response_data['courses']))

    def test_user_draft_tag_detail(self):
        resp = self.api_client.get(
            self.draft_tag_url, format='json', data=self.user_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('courses' in response_data)
        self.assertEqual(0, len(response_data['courses']))

    def test_manager_draft_tag_detail(self):
        resp = self.api_client.get(
            self.draft_tag_url, format='json', data=self.manager_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('courses' in response_data)
        self.assertEqual(1, len(response_data['courses']))

    def test_viewer_draft_tag_detail(self):
        resp = self.api_client.get(
            self.draft_tag_url, format='json', data=self.viewer_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('courses' in response_data)
        self.assertEqual(1, len(response_data['courses']))

    # check tag detail - live
    def test_admin_live_tag_detail(self):
        resp = self.api_client.get(
            self.live_tag_url, format='json', data=self.admin_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('courses' in response_data)
        self.assertEqual(3, len(response_data['courses']))

    def test_staff_live_tag_detail(self):
        resp = self.api_client.get(
            self.live_tag_url, format='json', data=self.staff_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('courses' in response_data)
        self.assertEqual(3, len(response_data['courses']))

    def test_teacher_live_tag_detail(self):
        resp = self.api_client.get(
            self.live_tag_url, format='json', data=self.teacher_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('courses' in response_data)
        self.assertEqual(2, len(response_data['courses']))

    def test_user_live_tag_detail(self):
        resp = self.api_client.get(
            self.live_tag_url, format='json', data=self.user_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('courses' in response_data)
        self.assertEqual(2, len(response_data['courses']))

    def test_manager_live_tag_detail(self):
        resp = self.api_client.get(
            self.live_tag_url, format='json', data=self.manager_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('courses' in response_data)
        self.assertEqual(3, len(response_data['courses']))

    def test_viewer_live_tag_detail(self):
        resp = self.api_client.get(
            self.live_tag_url, format='json', data=self.viewer_auth)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)
        response_data = self.deserialize(resp)
        self.assertTrue('courses' in response_data)
        self.assertEqual(3, len(response_data['courses']))

    # check course download pk - draft
    def test_draft_course_pk_download_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.draft_course_url_pk, format='json', data=self.admin_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_draft_course_pk_download_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.draft_course_url_pk, format='json', data=self.staff_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_draft_course_pk_download_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.draft_course_url_pk, format='json', data=self.teacher_auth)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_draft_course_pk_download_user(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.draft_course_url_pk, format='json', data=self.user_auth)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_draft_course_pk_download_manager(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.draft_course_url_pk, format='json', data=self.manager_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_draft_course_pk_download_viewer(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.draft_course_url_pk, format='json', data=self.viewer_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    # check course download pk - live
    def test_live_course_pk_download_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.live_course_url_pk, format='json', data=self.admin_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_live_course_pk_download_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.live_course_url_pk, format='json', data=self.staff_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_live_course_pk_download_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.live_course_url_pk, format='json', data=self.teacher_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_live_course_pk_download_user(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.live_course_url_pk, format='json', data=self.user_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_live_course_pk_download_manager(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.live_course_url_pk, format='json', data=self.manager_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_live_course_pk_download_viewer(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.live_course_url_pk, format='json', data=self.viewer_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    # check course download shortname live
    def test_live_course_shortname_download_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.live_course_url_shortname,
            format='json',
            data=self.admin_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_live_course_shortname_download_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.live_course_url_shortname,
            format='json',
            data=self.staff_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_live_course_shortname_download_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.live_course_url_shortname,
            format='json',
            data=self.teacher_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_live_course_shortname_download_user(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.live_course_url_shortname, format='json', data=self.user_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_live_course_shortname_download_manager(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.live_course_url_shortname,
            format='json',
            data=self.manager_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_live_course_shortname_download_viewer(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.live_course_url_shortname,
            format='json',
            data=self.viewer_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    # check course download shortname draft
    def test_draft_course_shortname_download_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.draft_course_url_shortname,
            format='json',
            data=self.admin_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_draft_course_shortname_download_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.draft_course_url_shortname,
            format='json',
            data=self.staff_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_draft_course_shortname_download_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.draft_course_url_shortname,
            format='json',
            data=self.teacher_auth)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_draft_course_shortname_download_user(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.draft_course_url_shortname,
            format='json',
            data=self.user_auth)
        self.assertEqual(response.status_code, 404)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    def test_draft_course_shortname_download_manager(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.draft_course_url_shortname,
            format='json',
            data=self.manager_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)

    def test_draft_course_shortname_download_viewer(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.api_client.get(
            self.draft_course_url_shortname,
            format='json',
            data=self.viewer_auth)
        self.assertHttpOK(response)
        self.assertEqual(response['content-type'],
                         self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start+1, tracker_count_end)
