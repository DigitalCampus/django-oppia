# tests/api/test_course_publish.py
import api
import pytest

from oppia.test import OppiaTransactionTestCase

from oppia.models import Course, CoursePublishingLog
from settings.models import SettingProperties


class CoursePublishResourceTest(OppiaTransactionTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']

    def setUp(self):
        super(CoursePublishResourceTest, self).setUp()
        self.url = '/api/publish/'
        self.course_file_path = \
            './oppia/fixtures/reference_files/ncd1_test_course.zip'
        self.video_file_path = \
            './oppia/fixtures/reference_files/sample_video.m4v'

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
    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
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

    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
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

    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
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

    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
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
    @pytest.mark.xfail(reason="works on local, but not on Github workflow \
        see issue: https://github.com/DigitalCampus/django-oppia/issues/689")
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
