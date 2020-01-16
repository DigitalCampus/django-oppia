import pytest

from django.urls import reverse
from oppia.test import OppiaTestCase


class CourseUploadTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']
    file_root = './oppia/fixtures/reference_files/'
    course_file_path = file_root + 'ncd1_test_course.zip'
    media_file_path = file_root + 'sample_video.m4v'
    empty_section_course = file_root + 'test_course_empty_section.zip'

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
            # should be redirected to the update step 2 form
            self.assertRedirects(response,
                                 reverse('oppia_upload2', args=[5]),
                                 302,
                                 200)
