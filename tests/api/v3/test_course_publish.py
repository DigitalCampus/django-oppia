import unittest
import os
import pytest

from rest_framework.test import APITestCase

from django.conf import settings

from oppia.models import Course, CourseStatus, CoursePublishingLog
from tests.api.v3 import utils
from settings.models import SettingProperties
from tests.utils import update_course_status


class CoursePublishAPITests(APITestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']

    url = '/api/v3/course/'
    course_file_field = 'course_file'
    no_module_xml = os.path.join(settings.TEST_RESOURCES, 'test_course_no_module_xml.zip')
    corrupt_course_zip = os.path.join(settings.TEST_RESOURCES, 'corrupt_course.zip')

    course_file_path = os.path.join(settings.TEST_RESOURCES, 'ncd1_test_course.zip')
    video_file_path = os.path.join(settings.TEST_RESOURCES, 'sample_video.m4v')
    course_draft_file_path = os.path.join(settings.TEST_RESOURCES, 'draft-20150611100319.zip')
    non_existing_course = os.path.join(settings.TEST_RESOURCES, 'test_course_empty_section.zip')
    non_existing_course_shortname = "empty-section"

    def publish_course(self, course_file, is_draft):
        response = self.client.post(self.url,
                                    {'username': 'admin',
                                     'password': 'password',
                                     'tags': 'demo',
                                     'is_draft': is_draft,
                                     self.course_file_field: course_file})
        return response

    # test all params have been sent
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_required_params(self):
        with open(self.course_file_path, 'rb') as course_file:
            # no username
            response = self.client.post(self.url,
                                        {'tags': 'demo',
                                         'password': 'secret',
                                         'is_draft': False,
                                         self.course_file_field: course_file})
        self.assertEqual(response.status_code, utils.HTTP_BAD_REQUEST)

        # no password
        with open(self.course_file_path, 'rb') as course_file:
            response = self.client.post(self.url,
                                        {'username': 'demo',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         self.course_file_field: course_file})
        self.assertEqual(response.status_code, utils.HTTP_BAD_REQUEST)

        # no tags
        with open(self.course_file_path, 'rb') as course_file:
            response = self.client.post(self.url,
                                        {'username': 'demo',
                                         'password': 'secret',
                                         'is_draft': False,
                                         self.course_file_field: course_file})
        self.assertEqual(response.status_code, utils.HTTP_BAD_REQUEST)

        # no is_draft
        with open(self.course_file_path, 'rb') as course_file:
            response = self.client.post(self.url,
                                        {'username': 'demo',
                                         'password': 'secret',
                                         'tags': 'demo',
                                         self.course_file_field: course_file})
        self.assertEqual(response.status_code, utils.HTTP_BAD_REQUEST)

    # test tags not empty
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_tags_not_empty(self):
        with open(self.course_file_path, 'rb') as course_file:
            response = self.client.post(self.url,
                                        {'username': 'admin',
                                         'password': 'password',
                                         'tags': '',
                                         'is_draft': False,
                                         self.course_file_field: course_file})
        self.assertEqual(response.status_code, utils.HTTP_BAD_REQUEST)

    # test is user has correct permissions or not to upload
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_upload_permission_admin(self):
        old_no_cpls = CoursePublishingLog.objects.filter(action='api_course_published').count()

        with open(self.course_file_path, 'rb') as course_file:
            # admin can upload
            response = self.client.post(self.url,
                                        {'username': 'admin',
                                         'password': 'password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         self.course_file_field: course_file})
        self.assertEqual(response.status_code, utils.HTTP_CREATED)

        # check record added to course publishing log
        new_no_cpls = CoursePublishingLog.objects.filter(action='api_course_published').count()
        self.assertEqual(old_no_cpls+1, new_no_cpls)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_upload_permission_staff(self):
        # set course owner to staff
        course = Course.objects.get(shortname='ncd1-et')
        original_user = course.user
        course.user = utils.get_staff_user()
        course.save()

        old_no_cpls = CoursePublishingLog.objects.filter(action='api_course_published').count()

        with open(self.course_file_path, 'rb') as course_file:
            # staff can upload
            response = self.client.post(self.url,
                                        {'username': 'staff',
                                         'password': 'password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         self.course_file_field: course_file})
        self.assertEqual(response.status_code, utils.HTTP_CREATED)

        # check record added to course publishing log
        new_no_cpls = CoursePublishingLog.objects.filter(action='api_course_published').count()
        self.assertEqual(old_no_cpls+1, new_no_cpls)

        # reset back to original owner
        course.user = original_user
        course.save()

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_upload_permission_teacher(self):
        # set course owner to teacher
        course = Course.objects.get(shortname='ncd1-et')
        original_user = course.user
        course.user = utils.get_teacher_user()
        course.save()

        old_no_cpls = CoursePublishingLog.objects.filter(action='api_course_published').count()

        with open(self.course_file_path, 'rb') as course_file:
            # teacher can upload
            response = self.client.post(self.url,
                                        {'username': 'teacher',
                                         'password': 'password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         self.course_file_field: course_file})
            self.assertEqual(response.status_code, utils.HTTP_CREATED)

            # check record added to course publishing log
            new_no_cpls = CoursePublishingLog.objects \
                .filter(action='api_course_published').count()
            self.assertEqual(old_no_cpls+1, new_no_cpls)

        # reset back to original owner
        course.user = original_user
        course.save()

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_upload_permission_user(self):

        old_no_cpls = CoursePublishingLog.objects.filter(action='api_course_published').count()

        with open(self.course_file_path, 'rb') as course_file:
            # normal user cannot upload
            response = self.client.post(self.url,
                                        {'username': 'demo',
                                         'password': 'password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         self.course_file_field: course_file})
            self.assertEqual(response.status_code, utils.HTTP_UNAUTHORIZED)

            # check record added to course publishing log
            new_no_cpls = CoursePublishingLog.objects.filter(action='api_course_published').count()
            self.assertEqual(old_no_cpls, new_no_cpls)

    # test user has given correct password
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_unauthorised_user(self):
        with open(self.course_file_path, 'rb') as course_file:
            # normal user cannot upload
            response = self.client.post(self.url,
                                        {'username': 'admin',
                                         'password': 'wrong_password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         self.course_file_field: course_file})
            self.assertEqual(response.status_code, utils.HTTP_UNAUTHORIZED)

    # test file is correct format
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_file_format(self):

        old_no_cpls = CoursePublishingLog.objects.filter(action='invalid_zip').count()

        with open(self.video_file_path, 'rb') as video_file:
            # send video file instead
            response = self.client.post(self.url,
                                        {'username': 'admin',
                                         'password': 'password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         self.course_file_field: video_file})
            self.assertEqual(response.status_code, utils.HTTP_BAD_REQUEST)

            # check record added to course publishing log
            new_no_cpls = CoursePublishingLog.objects.filter(action='invalid_zip').count()
            self.assertEqual(old_no_cpls+1, new_no_cpls)

    # test if user is trying to overwrite course they don't already own
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_overwriting_course_non_owner(self):
        # set course owner to admin
        course = Course.objects.get(shortname='anc1-all')
        original_user = course.user
        course.user = utils.get_admin_user()
        course.save()

        old_no_cpls = CoursePublishingLog.objects.filter(action='permissions_error').count()

        with open(self.course_file_path, 'rb') as course_file:
            # teacher attempts to update
            response = self.client.post(self.url,
                                        {'username': 'teacher',
                                         'password': 'password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         self.course_file_field: course_file})
            self.assertEqual(response.status_code, utils.HTTP_UNAUTHORIZED)

            # check record added to course publishing log

            new_no_cpls = CoursePublishingLog.objects.filter(action='permissions_error').count()
            self.assertEqual(old_no_cpls+1, new_no_cpls)

        # reset back to original owner
        course.user = original_user
        course.save()

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_overwriting_course_manager(self):
        # set course owner to admin
        course = Course.objects.get(shortname='draft-test')
        original_user = course.user
        course.user = utils.get_admin_user()
        course.save()

        old_no_cpls = CoursePublishingLog.objects.filter(action='permissions_error').count()

        with open(self.course_draft_file_path, 'rb') as course_file:
            # teacher attempts to update
            response = self.client.post(self.url,
                                        {'username': 'manager',
                                         'password': 'manager',
                                         'tags': 'draft',
                                         'is_draft': True,
                                         self.course_file_field: course_file})
            self.assertEqual(response.status_code, utils.HTTP_CREATED)

            # check record added to course publishing log
            new_no_cpls = CoursePublishingLog.objects.filter(action='permissions_error').count()
            self.assertEqual(old_no_cpls, new_no_cpls)

            # check user changed
            course = Course.objects.get(shortname='draft-test')
            self.assertEqual(course.user.username, 'manager')

        # reset back to original owner
        course.user = original_user
        course.save()

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_overwriting_course_viewer(self):
        # set course owner to admin
        course = Course.objects.get(shortname='draft-test')
        original_user = course.user
        course.user = utils.get_admin_user()
        course.save()

        old_no_cpls = CoursePublishingLog.objects.filter(action='permissions_error').count()

        with open(self.course_file_path, 'rb') as course_file:
            # teacher attempts to update
            response = self.client.post(self.url,
                                        {'username': 'viewer',
                                         'password': 'viewer',
                                         'tags': 'draft',
                                         'is_draft': False,
                                         self.course_file_field: course_file})
            self.assertEqual(response.status_code, utils.HTTP_UNAUTHORIZED)

            # check record added to course publishing log

            new_no_cpls = CoursePublishingLog.objects.filter(action='permissions_error').count()
            self.assertEqual(old_no_cpls+1, new_no_cpls)

        # reset back to original owner
        course.user = original_user
        course.save()

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_overwriting_course_viewer_draft_true(self):
        # set course owner to admin
        course = Course.objects.get(shortname='draft-test')
        original_user = course.user
        course.user = utils.get_admin_user()
        course.save()

        old_no_cpls = CoursePublishingLog.objects.filter(action='permissions_error').count()

        with open(self.course_draft_file_path, 'rb') as course_file:
            # teacher attempts to update
            response = self.client.post(self.url,
                                        {'username': 'viewer',
                                         'password': 'viewer',
                                         'tags': 'draft',
                                         'is_draft': True,
                                         self.course_file_field: course_file})
            self.assertEqual(response.status_code, utils.HTTP_UNAUTHORIZED)

            # check record added to course publishing log

            new_no_cpls = CoursePublishingLog.objects.filter(action='permissions_error').count()
            self.assertEqual(old_no_cpls+1, new_no_cpls)

        # reset back to original owner
        course.user = original_user
        course.save()

    # check file size of course
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_course_filesize_limit(self):
        setting, created = SettingProperties.objects.get_or_create(key='MAX_UPLOAD_SIZE')
        setting.int_value = 1000
        setting.save()

        old_no_cpls = CoursePublishingLog.objects.filter(action='over_max_upload').count()

        with open(self.course_file_path, 'rb') as course_file:
            response = self.client.post(self.url,
                                        {'username': 'admin',
                                         'password': 'password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         self.course_file_field: course_file})
            self.assertEqual(response.status_code, utils.HTTP_BAD_REQUEST)

            # check record added to course publishing log
            new_no_cpls = CoursePublishingLog.objects.filter(action='over_max_upload').count()
            self.assertEqual(old_no_cpls+1, new_no_cpls)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_course_invalid_xml(self):

        old_no_cpls = CoursePublishingLog.objects.filter(action='no_module_xml').count()

        with open(self.no_module_xml, 'rb') as course_file:
            response = self.client.post(self.url,
                                        {'username': 'admin',
                                         'password': 'password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         self.course_file_field: course_file})

            self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
            new_no_cpls = CoursePublishingLog.objects.filter(action='no_module_xml').count()
            self.assertEqual(old_no_cpls+2, new_no_cpls)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_get_course_bad_zip(self):

        old_no_cpls = CoursePublishingLog.objects.filter(action='invalid_zip').count()

        with open(self.corrupt_course_zip, 'rb') as course_file:
            response = self.client.post(self.url,
                                        {'username': 'admin',
                                         'password': 'password',
                                         'tags': 'demo',
                                         'is_draft': False,
                                         self.course_file_field: course_file})

            self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
            new_no_cpls = CoursePublishingLog.objects.filter(action='invalid_zip').count()
            self.assertEqual(old_no_cpls+2, new_no_cpls)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_publish_new_live_course(self):
        with open(self.non_existing_course, 'rb') as course_file:
            response = self.publish_course(course_file, False)
            self.assertEqual(response.status_code, utils.HTTP_CREATED)

            course = Course.objects.get(shortname=self.non_existing_course_shortname)
            self.assertEqual(CourseStatus.LIVE, course.status)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_publish_live_course_when_live_course_exists_should_publish(self):
        course_id = 2
        original_status = update_course_status(course_id, CourseStatus.LIVE)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, False)
            self.assertEqual(response.status_code, utils.HTTP_CREATED)

            course = Course.objects.latest('lastupdated_date')
            self.assertEqual(course_id, course.pk)
            self.assertEqual(CourseStatus.LIVE, course.status)

        # reset back to original status
        update_course_status(course_id, original_status)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_publish_live_course_when_draft_course_exists_should_not_publish(self):
        course_id = 2
        original_status = update_course_status(course_id, CourseStatus.DRAFT)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, False)
            self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)

            course = Course.objects.get(pk=course_id)
            self.assertEqual(CourseStatus.DRAFT, course.status)

        # reset back to original status
        update_course_status(course_id, original_status)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_publish_live_course_when_newdownloadsdisabled_course_exists_should_not_publish(self):
        course_id = 2
        original_status = update_course_status(course_id, CourseStatus.NEW_DOWNLOADS_DISABLED)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, False)
            self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)

            course = Course.objects.get(pk=course_id)
            self.assertEqual(CourseStatus.NEW_DOWNLOADS_DISABLED, course.status)

        # reset back to original status
        update_course_status(course_id, original_status)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_publish_live_course_when_archived_course_exists_should_not_publish(self):
        course_id = 2
        original_status = update_course_status(course_id, CourseStatus.ARCHIVED)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, False)
            self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)

            course = Course.objects.get(pk=course_id)
            self.assertEqual(CourseStatus.ARCHIVED, course.status)

        # reset back to original status
        update_course_status(course_id, original_status)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_publish_live_course_when_readonly_course_exists_should_not_publish(self):
        course_id = 2
        original_status = update_course_status(course_id, CourseStatus.READ_ONLY)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, False)
            self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)

            course = Course.objects.get(pk=course_id)
            self.assertEqual(CourseStatus.READ_ONLY, course.status)

        # reset back to original status
        update_course_status(course_id, original_status)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_publish_new_draft_course(self):
        with open(self.non_existing_course, 'rb') as course_file:
            response = self.publish_course(course_file, True)
            self.assertEqual(response.status_code, utils.HTTP_CREATED)

            course = Course.objects.get(shortname=self.non_existing_course_shortname)
            self.assertEqual(CourseStatus.DRAFT, course.status)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_publish_draft_course_when_live_course_exists_should_publish_and_update_status(self):
        course_id = 2
        original_status = update_course_status(course_id, CourseStatus.LIVE)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, True)
            self.assertEqual(response.status_code, utils.HTTP_CREATED)

            course = Course.objects.get(pk=course_id)
            self.assertEqual("ncd1-et", course.shortname)
            self.assertEqual(course_id, course.pk)
            self.assertEqual(CourseStatus.DRAFT, course.status)

        # reset back to original status
        update_course_status(course_id, original_status)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_publish_draft_course_when_draft_course_exists_should_publish(self):
        course_id = 2
        original_status = update_course_status(course_id, CourseStatus.DRAFT)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, True)
            self.assertEqual(response.status_code, utils.HTTP_CREATED)

            course = Course.objects.latest('lastupdated_date')
            self.assertEqual(course_id, course.pk)
            self.assertEqual(CourseStatus.DRAFT, course.status)

        # reset back to original status
        update_course_status(course_id, original_status)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_publish_draft_course_when_newdownloadsdisabled_course_exists_should_not_publish(self):
        course_id = 2
        original_status = update_course_status(course_id, CourseStatus.NEW_DOWNLOADS_DISABLED)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, True)
            self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)

            course = Course.objects.get(pk=course_id)
            self.assertEqual(CourseStatus.NEW_DOWNLOADS_DISABLED, course.status)

        # reset back to original status
        update_course_status(course_id, original_status)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_publish_draft_course_when_archived_course_exists_should_not_publish(self):
        course_id = 2
        original_status = update_course_status(course_id, CourseStatus.ARCHIVED)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, True)
            self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)

            course = Course.objects.get(pk=course_id)
            self.assertEqual(CourseStatus.ARCHIVED, course.status)

        # reset back to original status
        update_course_status(course_id, original_status)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_publish_draft_course_when_readonly_course_exists_should_not_publish(self):
        course_id = 2
        original_status = update_course_status(course_id, CourseStatus.READ_ONLY)

        with open(self.course_file_path, 'rb') as course_file:
            response = self.publish_course(course_file, True)
            self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)

            course = Course.objects.get(pk=course_id)
            self.assertEqual(CourseStatus.READ_ONLY, course.status)

        # reset back to original status
        update_course_status(course_id, original_status)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_publish_draft_course_when_draft_status_is_available_should_publish(self):
        initial_course_count = Course.objects.count()
        original_available_statuses = settings.OPPIA_AVAILABLE_COURSE_STATUSES
        settings.OPPIA_AVAILABLE_COURSE_STATUSES = ['draft']

        with open(self.non_existing_course, 'rb') as course_file:
            response = self.publish_course(course_file, True)
            self.assertEqual(response.status_code, utils.HTTP_CREATED)
            course = Course.objects.latest('created_date')
            self.assertEqual(self.non_existing_course_shortname, course.shortname)
            self.assertEqual(CourseStatus.DRAFT, course.status)

            self.assertEqual(initial_course_count + 1, Course.objects.count())

        settings.OPPIA_AVAILABLE_COURSE_STATUSES = original_available_statuses

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_publish_draft_course_when_draft_status_is_not_available_should_not_publish(self):
        initial_course_count = Course.objects.count()
        original_available_statuses = settings.OPPIA_AVAILABLE_COURSE_STATUSES

        # @TODO remove comment when test enabled
        # settings.OPPIA_AVAILABLE_COURSE_STATUSES = ['live', 'archived']

        with open(self.non_existing_course, 'rb') as course_file:
            response = self.publish_course(course_file, True)
            self.assertEqual(utils.HTTP_BAD_REQUEST, response.status_code)
            self.assertEqual(initial_course_count, Course.objects.count())

        settings.OPPIA_AVAILABLE_COURSE_STATUSES = original_available_statuses
