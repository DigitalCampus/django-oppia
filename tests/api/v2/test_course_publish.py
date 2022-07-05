# tests/api/test_course_publish.py
import os

import api

from django.conf import settings
from django.test.client import RequestFactory

from oppia.test import OppiaTransactionTestCase

from oppia.models import Course, CoursePublishingLog, CourseStatus
from settings.models import SettingProperties
from tests.utils import update_course_status


class CoursePublishResourceTest(OppiaTransactionTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_course_statuses.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']

    no_module_xml = os.path.join(settings.TEST_RESOURCES, 'test_course_no_module_xml.zip')
    corrupt_course_zip = os.path.join(settings.TEST_RESOURCES, 'corrupt_course.zip')

    def setUp(self):
        super(CoursePublishResourceTest, self).setUp()
        self.factory = RequestFactory()
        self.url = '/api/publish/'
        self.course_file_path = os.path.join(settings.TEST_RESOURCES, 'ncd1_test_course.zip')
        self.video_file_path = os.path.join(settings.TEST_RESOURCES, 'sample_video.m4v')
        self.course_draft_file_path = os.path.join(settings.TEST_RESOURCES, 'draft-20150611100319.zip')
        self.non_existing_course = os.path.join(settings.TEST_RESOURCES, 'test_course_empty_section.zip')
        self.non_existing_course_shortname = "empty-section"

    def publish_course(self, course_file, is_draft):
        response = self.client.post(self.url,
                                    {'username': 'admin',
                                     'password': 'password',
                                     'tags': 'demo',
                                     'is_draft': is_draft,
                                     api.COURSE_FILE_FIELD: course_file})
        return response

    # test only POST is available
    def test_no_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    # test all params have been sent
    def test_required_params(self):
        with open(self.course_file_path, 'rb') as course_file:
            # no username
            response = self.client.post(self.url,
                                        {'tags': 'demo',
                                         'password': 'secret',
                                         'is_draft': False,
                                         api.COURSE_FILE_FIELD: course_file})
        self.assertEqual(response.status_code, 400)

        # no password
        with open(self.course_file_path, 'rb') as course_file:
            response = self.client.post(self.url,
                                        {'username': 'demo',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         api.COURSE_FILE_FIELD: course_file})
        self.assertEqual(response.status_code, 400)

        # no tags
        with open(self.course_file_path, 'rb') as course_file:
            response = self.client.post(self.url,
                                        {'username': 'demo',
                                         'password': 'secret',
                                         'is_draft': False,
                                         api.COURSE_FILE_FIELD: course_file})
        self.assertEqual(response.status_code, 400)

        # no is_draft
        with open(self.course_file_path, 'rb') as course_file:
            response = self.client.post(self.url,
                                        {'username': 'demo',
                                         'password': 'secret',
                                         'tags': 'demo',
                                         api.COURSE_FILE_FIELD: course_file})
        self.assertEqual(response.status_code, 400)

    # test tags not empty
    def test_tags_not_empty(self):
        with open(self.course_file_path, 'rb') as course_file:
            response = self.client.post(self.url,
                                        {'username': 'admin',
                                         'password': 'password',
                                         'tags': '',
                                         'is_draft': False,
                                         api.COURSE_FILE_FIELD: course_file})
        self.assertEqual(response.status_code, 400)

    # test is user has correct permissions or not to upload
    def test_upload_permission_admin(self):
        old_no_cpls = CoursePublishingLog.objects \
            .filter(action='api_course_published').count()

        with open(self.course_file_path, 'rb') as course_file:
            # admin can upload
            response = self.client.post(self.url,
                                        {'username': 'admin',
                                         'password': 'password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         api.COURSE_FILE_FIELD: course_file})
        self.assertEqual(response.status_code, 201)

        # check record added to course publishing log
        new_no_cpls = CoursePublishingLog.objects \
            .filter(action='api_course_published').count()
        self.assertEqual(old_no_cpls+1, new_no_cpls)

    def test_upload_permission_staff(self):
        # set course owner to staff
        course = Course.objects.get(shortname='ncd1-et')
        course.user = self.staff_user
        course.save()

        old_no_cpls = CoursePublishingLog.objects \
            .filter(action='api_course_published').count()

        with open(self.course_file_path, 'rb') as course_file:
            # staff can upload
            response = self.client.post(self.url,
                                        {'username': 'staff',
                                         'password': 'password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         api.COURSE_FILE_FIELD: course_file})
        self.assertEqual(response.status_code, 201)

        # check record added to course publishing log
        new_no_cpls = CoursePublishingLog.objects \
            .filter(action='api_course_published').count()
        self.assertEqual(old_no_cpls+1, new_no_cpls)

    def test_upload_permission_teacher(self):
        # set course owner to teacher
        course = Course.objects.get(shortname='ncd1-et')
        course.user = self.teacher_user
        course.save()

        old_no_cpls = CoursePublishingLog.objects \
            .filter(action='api_course_published').count()

        with open(self.course_file_path, 'rb') as course_file:
            # teacher can upload
            response = self.client.post(self.url,
                                        {'username': 'teacher',
                                         'password': 'password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         api.COURSE_FILE_FIELD: course_file})
            self.assertEqual(response.status_code, 201)

            # check record added to course publishing log
            new_no_cpls = CoursePublishingLog.objects \
                .filter(action='api_course_published').count()
            self.assertEqual(old_no_cpls+1, new_no_cpls)

    def test_upload_permission_user(self):

        old_no_cpls = CoursePublishingLog.objects \
            .filter(action='api_course_published').count()

        with open(self.course_file_path, 'rb') as course_file:
            # normal user cannot upload
            response = self.client.post(self.url,
                                        {'username': 'demo',
                                         'password': 'password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         api.COURSE_FILE_FIELD: course_file})
            self.assertEqual(response.status_code, 401)

            # check record added to course publishing log
            new_no_cpls = CoursePublishingLog.objects \
                .filter(action='api_course_published').count()
            self.assertEqual(old_no_cpls, new_no_cpls)

    # test user has given correct password
    def test_unauthorised_user(self):
        with open(self.course_file_path, 'rb') as course_file:
            # normal user cannot upload
            response = self.client.post(self.url,
                                        {'username': 'admin',
                                         'password': 'wrong_password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         api.COURSE_FILE_FIELD: course_file})
            self.assertEqual(response.status_code, 401)

    # test file is correct format
    def test_file_format(self):

        old_no_cpls = CoursePublishingLog.objects \
            .filter(action='invalid_zip').count()

        with open(self.video_file_path, 'rb') as video_file:
            # send video file instead
            response = self.client.post(self.url,
                                        {'username': 'admin',
                                         'password': 'password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         api.COURSE_FILE_FIELD: video_file})
            self.assertEqual(response.status_code, 400)

            # check record added to course publishing log
            new_no_cpls = CoursePublishingLog.objects \
                .filter(action='invalid_zip').count()
            self.assertEqual(old_no_cpls+1, new_no_cpls)

    # test if user is trying to overwrite course they don't already own
    def test_overwriting_course_non_owner(self):
        # set course owner to admin
        course = Course.objects.get(shortname='anc1-all')
        course.user = self.admin_user
        course.save()

        old_no_cpls = CoursePublishingLog.objects \
            .filter(action='permissions_error').count()

        with open(self.course_file_path, 'rb') as course_file:
            # teacher attempts to update
            response = self.client.post(self.url,
                                        {'username': 'teacher',
                                         'password': 'password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         api.COURSE_FILE_FIELD: course_file})
            self.assertEqual(response.status_code, 401)

            # check record added to course publishing log

            new_no_cpls = CoursePublishingLog.objects \
                .filter(action='permissions_error').count()
            self.assertEqual(old_no_cpls+1, new_no_cpls)

    def test_overwriting_course_manager(self):
        # set course owner to admin
        course = Course.objects.get(shortname='draft-test')
        course.user = self.admin_user
        course.save()

        old_no_cpls = CoursePublishingLog.objects \
            .filter(action='permissions_error').count()

        with open(self.course_draft_file_path, 'rb') as course_file:
            # teacher attempts to update
            response = self.client.post(self.url,
                                        {'username': 'manager',
                                         'password': 'manager',
                                         'tags': 'draft',
                                         'is_draft': True,
                                         api.COURSE_FILE_FIELD: course_file})
            self.assertEqual(response.status_code, 201)

            # check record added to course publishing log
            new_no_cpls = CoursePublishingLog.objects \
                .filter(action='permissions_error').count()
            self.assertEqual(old_no_cpls, new_no_cpls)

            # check user changed
            course = Course.objects.get(shortname='draft-test')
            self.assertEqual(course.user.username, 'manager')

    def test_overwriting_course_viewer(self):
        # set course owner to admin
        course = Course.objects.get(shortname='draft-test')
        course.user = self.admin_user
        course.save()

        old_no_cpls = CoursePublishingLog.objects \
            .filter(action='permissions_error').count()

        with open(self.course_file_path, 'rb') as course_file:
            # teacher attempts to update
            response = self.client.post(self.url,
                                        {'username': 'viewer',
                                         'password': 'viewer',
                                         'tags': 'draft',
                                         'is_draft': False,
                                         api.COURSE_FILE_FIELD: course_file})
            self.assertEqual(response.status_code, 401)

            # check record added to course publishing log

            new_no_cpls = CoursePublishingLog.objects \
                .filter(action='permissions_error').count()
            self.assertEqual(old_no_cpls+1, new_no_cpls)

    def test_overwriting_course_viewer_draft_true(self):
        # set course owner to admin
        course = Course.objects.get(shortname='draft-test')
        course.user = self.admin_user
        course.save()

        old_no_cpls = CoursePublishingLog.objects \
            .filter(action='permissions_error').count()

        with open(self.course_draft_file_path, 'rb') as course_file:
            # teacher attempts to update
            response = self.client.post(self.url,
                                        {'username': 'viewer',
                                         'password': 'viewer',
                                         'tags': 'draft',
                                         'is_draft': True,
                                         api.COURSE_FILE_FIELD: course_file})
            self.assertEqual(response.status_code, 401)

            # check record added to course publishing log

            new_no_cpls = CoursePublishingLog.objects \
                .filter(action='permissions_error').count()
            self.assertEqual(old_no_cpls+1, new_no_cpls)

    # check file size of course
    def test_course_filesize_limit(self):
        setting, created = SettingProperties.objects \
            .get_or_create(key='MAX_UPLOAD_SIZE')
        setting.int_value = 1000
        setting.save()

        old_no_cpls = CoursePublishingLog.objects \
            .filter(action='over_max_upload').count()

        with open(self.course_file_path, 'rb') as course_file:
            response = self.client.post(self.url,
                                        {'username': 'admin',
                                         'password': 'password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         api.COURSE_FILE_FIELD: course_file})
            self.assertEqual(response.status_code, 400)

            # check record added to course publishing log
            new_no_cpls = CoursePublishingLog.objects \
                .filter(action='over_max_upload').count()
            self.assertEqual(old_no_cpls+1, new_no_cpls)

    def test_get_course_invalid_xml(self):

        old_no_cpls = CoursePublishingLog.objects \
            .filter(action='no_module_xml').count()

        with open(self.no_module_xml, 'rb') as course_file:
            response = self.client.post(self.url,
                                        {'username': 'admin',
                                         'password': 'password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         api.COURSE_FILE_FIELD: course_file})

            self.assertEqual(400, response.status_code)
            new_no_cpls = CoursePublishingLog.objects \
                .filter(action='no_module_xml').count()
            self.assertEqual(old_no_cpls+2, new_no_cpls)

    def test_get_course_bad_zip(self):

        old_no_cpls = CoursePublishingLog.objects \
            .filter(action='invalid_zip').count()

        with open(self.corrupt_course_zip, 'rb') as course_file:
            response = self.client.post(self.url,
                                        {'username': 'admin',
                                         'password': 'password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         api.COURSE_FILE_FIELD: course_file})

            self.assertEqual(500, response.status_code)
            new_no_cpls = CoursePublishingLog.objects \
                .filter(action='invalid_zip').count()
            self.assertEqual(old_no_cpls+2, new_no_cpls)

    def test_publish_new_live_course(self):
        with open(self.non_existing_course, 'rb') as course_file:
            response = self.publish_course(course_file, False)
            self.assertEqual(201, response.status_code)

            course = Course.objects.get(shortname=self.non_existing_course_shortname)
            self.assertEqual(CourseStatus.LIVE, course.status.name)

    def test_publish_live_course_when_live_course_exists__should_publish(self):
        update_course_status(2, CourseStatus.LIVE)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, False)
            self.assertEqual(201, response.status_code)

    def test_publish_live_course_when_draft_course_exists__should_not_publish(self):
        update_course_status(2, CourseStatus.DRAFT)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, False)
            self.assertEqual(400, response.status_code)

    def test_publish_live_course_when_newdownloadsdisabled_course_exists__should_not_publish(self):
        update_course_status(2, CourseStatus.NEW_DOWNLOADS_DISABLED)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, False)
            self.assertEqual(400, response.status_code)

    def test_publish_live_course_when_archived_course_exists__should_not_publish(self):
        update_course_status(2, CourseStatus.ARCHIVED)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, False)
            self.assertEqual(400, response.status_code)

    def test_publish_live_course_when_readonly_course_exists__should_not_publish(self):
        update_course_status(2, CourseStatus.READ_ONLY)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, False)
            self.assertEqual(400, response.status_code)

    def test_publish_new_draft_course(self):
        with open(self.non_existing_course, 'rb') as course_file:
            response = self.publish_course(course_file, True)
            self.assertEqual(201, response.status_code)

            course = Course.objects.get(shortname=self.non_existing_course_shortname)
            self.assertEqual(CourseStatus.DRAFT, course.status.name)

    def test_publish_draft_course_when_live_course_exists__should_publish_and_update_status(self):
        course_id = 2
        update_course_status(course_id, CourseStatus.LIVE)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, True)
            self.assertEqual(201, response.status_code)

            course = Course.objects.get(pk=course_id)
            self.assertEqual(CourseStatus.DRAFT, course.status.name)

    def test_publish_draft_course_when_draft_course_exists__should_publish(self):
        update_course_status(2, CourseStatus.DRAFT)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, True)
            self.assertEqual(201, response.status_code)

    def test_publish_draft_course_when_newdownloadsdisabled_course_exists__should_not_publish(self):
        update_course_status(2, CourseStatus.NEW_DOWNLOADS_DISABLED)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, True)
            self.assertEqual(400, response.status_code)

    def test_publish_draft_course_when_archived_course_exists__should_not_publish(self):
        update_course_status(2, CourseStatus.ARCHIVED)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, True)
            self.assertEqual(400, response.status_code)

    def test_publish_draft_course_when_readonly_course_exists__should_not_publish(self):
        update_course_status(2, CourseStatus.READ_ONLY)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, True)
            self.assertEqual(400, response.status_code)
