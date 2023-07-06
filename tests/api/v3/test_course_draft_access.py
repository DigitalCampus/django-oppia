import unittest
import pytest

from rest_framework.test import APITestCase

from oppia.models import Tracker
from tests.api.v3 import utils


class DraftCourseAccessAPITests(APITestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']

    STR_ZIP_EXPECTED_CONTENT_TYPE = 'application/zip'
    TEST_COURSES = ['anc_test_course.zip', 'draft-20150611100319.zip']

    live_course_url_pk = "/api/v3/course/1/download/"
    draft_course_url_pk = "/api/v3/course/3/download/"
    live_course_url_shortname = "/api/v3/course/anc1-all/download/"
    draft_course_url_shortname = "/api/v3/course/draft-test/download/"
    category_url = "/api/v3/category/"
    draft_category_url = "/api/v3/category/8/"
    live_category_url = "/api/v3/category/1/"

    def setUp(self):
        super(DraftCourseAccessAPITests, self).setUp()
        utils.copy_test_courses(self.TEST_COURSES)

    # check the tag listings
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_admin_tags(self):
        response = self.client.get(self.category_url, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        categories = response.json()
        self.assertEqual(6, len(categories))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_staff_tags(self):
        response = self.client.get(self.category_url, utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        categories = response.json()
        self.assertEqual(6, len(categories))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_teacher_tags(self):
        response = self.client.get(self.category_url, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        categories = response.json()
        self.assertEqual(5, len(categories))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_user_tags(self):
        response = self.client.get(self.category_url, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        categories = response.json()
        self.assertEqual(5, len(categories))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_manager_tags(self):
        response = self.client.get(self.category_url, utils.get_auth_header_manager())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        categories = response.json()
        self.assertEqual(6, len(categories))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_viewer_tags(self):
        response = self.client.get(self.category_url, utils.get_auth_header_viewer())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        categories = response.json()
        self.assertEqual(6, len(categories))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    # check tag detail - draft
    def test_admin_draft_tag_detail(self):
        response = self.client.get(self.draft_category_url, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        category = response.json()
        self.assertTrue('courses' in category)
        self.assertEqual(1, len(category['courses']))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_staff_draft_tag_detail(self):
        response = self.client.get(self.draft_category_url, utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        category = response.json()
        self.assertTrue('courses' in category)
        self.assertEqual(1, len(category['courses']))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_teacher_draft_tag_detail(self):
        response = self.client.get(self.draft_category_url, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        category = response.json()
        self.assertTrue('courses' in category)
        self.assertEqual(0, len(category['courses']))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_user_draft_tag_detail(self):
        response = self.client.get(self.draft_category_url, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        category = response.json()
        self.assertTrue('courses' in category)
        self.assertEqual(0, len(category['courses']))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_manager_draft_tag_detail(self):
        response = self.client.get(self.draft_category_url, utils.get_auth_header_manager())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        category = response.json()
        self.assertTrue('courses' in category)
        self.assertEqual(1, len(category['courses']))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_viewer_draft_tag_detail(self):
        response = self.client.get(self.draft_category_url, utils.get_auth_header_viewer())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        category = response.json()
        self.assertTrue('courses' in category)
        self.assertEqual(1, len(category['courses']))

    # check tag detail - live
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_admin_live_tag_detail(self):
        response = self.client.get(self.live_category_url, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        category = response.json()
        self.assertTrue('courses' in category)
        self.assertEqual(3, len(category['courses']))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_staff_live_tag_detail(self):
        response = self.client.get(self.live_category_url, utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        category = response.json()
        self.assertTrue('courses' in category)
        self.assertEqual(3, len(category['courses']))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_teacher_live_tag_detail(self):
        response = self.client.get(self.live_category_url, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        category = response.json()
        self.assertTrue('courses' in category)
        self.assertEqual(2, len(category['courses']))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_user_live_tag_detail(self):
        response = self.client.get(self.live_category_url, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        category = response.json()
        self.assertTrue('courses' in category)
        self.assertEqual(2, len(category['courses']))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_manager_live_tag_detail(self):
        response = self.client.get(self.live_category_url, utils.get_auth_header_manager())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        category = response.json()
        self.assertTrue('courses' in category)
        self.assertEqual(3, len(category['courses']))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_viewer_live_tag_detail(self):
        response = self.client.get(self.live_category_url, utils.get_auth_header_viewer())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        category = response.json()
        self.assertTrue('courses' in category)
        self.assertEqual(2, len(category['courses']))

    # check course download pk - draft
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_pk_download_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.draft_course_url_pk, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_pk_download_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.draft_course_url_pk, utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_pk_download_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.draft_course_url_pk, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_pk_download_user(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.draft_course_url_pk, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_pk_download_manager(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.draft_course_url_pk, utils.get_auth_header_manager())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_pk_download_viewer(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.draft_course_url_pk, utils.get_auth_header_viewer())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    # check course download pk - live
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_live_course_pk_download_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.live_course_url_pk, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_live_course_pk_download_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.live_course_url_pk, utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_live_course_pk_download_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.live_course_url_pk, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_live_course_pk_download_user(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.live_course_url_pk, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_live_course_pk_download_manager(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.live_course_url_pk, utils.get_auth_header_manager())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_live_course_pk_download_viewer(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.live_course_url_pk, utils.get_auth_header_viewer())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    # check course download shortname live
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_live_course_shortname_download_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.live_course_url_shortname, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_live_course_shortname_download_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.live_course_url_shortname, utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_live_course_shortname_download_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.live_course_url_shortname, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_live_course_shortname_download_user(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.live_course_url_shortname, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_live_course_shortname_download_manager(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.live_course_url_shortname, utils.get_auth_header_manager())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_live_course_shortname_download_viewer(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.live_course_url_shortname, utils.get_auth_header_viewer())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    # check course download shortname draft
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_shortname_download_admin(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.draft_course_url_shortname, utils.get_auth_header_admin())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_shortname_download_staff(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.draft_course_url_shortname, utils.get_auth_header_staff())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_shortname_download_teacher(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.draft_course_url_shortname, utils.get_auth_header_teacher())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_shortname_download_user(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.draft_course_url_shortname, utils.get_auth_header_user())
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_shortname_download_manager(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.draft_course_url_shortname, utils.get_auth_header_manager())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_draft_course_shortname_download_viewer(self):
        tracker_count_start = Tracker.objects.all().count()
        response = self.client.get(self.draft_course_url_shortname, utils.get_auth_header_viewer())
        self.assertEqual(response.status_code, utils.HTTP_OK)
        self.assertEqual(response['content-type'], self.STR_ZIP_EXPECTED_CONTENT_TYPE)
        tracker_count_end = Tracker.objects.all().count()
        self.assertEqual(tracker_count_start, tracker_count_end)
