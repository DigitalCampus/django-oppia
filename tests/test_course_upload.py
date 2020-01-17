import pytest

from django.urls import reverse
from oppia.test import OppiaTestCase
from oppia.models import Course, CoursePublishingLog
from zipfile import BadZipfile


class CourseUploadTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']
    file_root = './oppia/fixtures/reference_files/'
    course_file_path = file_root + 'ncd1_test_course.zip'
    media_file_path = file_root + 'sample_video.m4v'
    empty_section_course = file_root + 'test_course_empty_section.zip'
    no_module_xml = file_root + 'test_course_no_module_xml.zip'
    corrupt_course_zip = file_root + 'corrupt_course.zip'
    course_no_sub_dir = file_root + 'test_course_no_sub_dir.zip'

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_upload_template(self):

        with open(self.course_file_path, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(reverse('oppia_upload'),
                                        {'course_file': course_file})
            # should be redirected to the update step 2 form
            self.assertRedirects(response,
                                 reverse('oppia_upload2', args=[2]),
                                 302,
                                 200)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_upload_with_empty_sections(self):

        with open(self.empty_section_course, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(reverse('oppia_upload'),
                                        {'course_file': course_file})

            course = Course.objects.latest('created_date')
            # should be redirected to the update step 2 form
            self.assertRedirects(response,
                                 reverse('oppia_upload2', args=[course.id]),
                                 302,
                                 200)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_upload_no_module_xml(self):

        with open(self.no_module_xml, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(reverse('oppia_upload'),
                                        {'course_file': course_file})

            self.assertEqual(200, response.status_code)
            course_log = CoursePublishingLog.objects.latest('log_date')
            self.assertEqual("no_module_xml", course_log.action)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_corrupt_course(self):

        with open(self.corrupt_course_zip, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(reverse('oppia_upload'),
                                        {'course_file': course_file})

            self.assertEqual(200, response.status_code)
            self.assertRaises(BadZipfile)
            course_log = CoursePublishingLog.objects.latest('log_date')
            self.assertEqual("invalid_zip", course_log.action)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_no_sub_dir(self):

        with open(self.course_no_sub_dir, 'rb') as course_file:
            self.client.force_login(self.admin_user)
            response = self.client.post(reverse('oppia_upload'),
                                        {'course_file': course_file})

            self.assertEqual(200, response.status_code)
            course_log = CoursePublishingLog.objects.latest('log_date')
            self.assertEqual("invalid_zip", course_log.action)
