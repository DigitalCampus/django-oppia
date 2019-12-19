import pytest

from django.urls import reverse
from oppia.test import OppiaTestCase


class CourseUploadTest(OppiaTestCase):

    course_file_path = './oppia/fixtures/reference_files/ncd1_test_course.zip'
    media_file_path = './oppia/fixtures/reference_files/sample_video.m4v'

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
