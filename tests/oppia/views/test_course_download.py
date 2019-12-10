import pytest

from django.urls import reverse
from django.test import TestCase

from tests.user_logins import ADMIN_USER, \
                              STAFF_USER, \
                              NORMAL_USER, \
                              TEACHER_USER
from tests.utils import update_course_visibility


class DownloadViewTest(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']

    STR_EXPECTED_CONTENT_TYPE = 'application/zip'

    def setUp(self):
        super(DownloadViewTest, self).setUp()

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_live_course_admin(self):
        self.client.login(username=ADMIN_USER['user'],
                          password=ADMIN_USER['password'])
        url = reverse('oppia_course_download', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_live_course_staff(self):
        self.client.login(username=STAFF_USER['user'],
                          password=STAFF_USER['password'])
        url = reverse('oppia_course_download', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_live_course_teacher(self):
        self.client.login(username=TEACHER_USER['user'],
                          password=TEACHER_USER['password'])
        url = reverse('oppia_course_download', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_live_course_normal(self):
        self.client.login(username=NORMAL_USER['user'],
                          password=NORMAL_USER['password'])
        url = reverse('oppia_course_download', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_draft_course_admin(self):
        update_course_visibility(1, True, False)
        self.client.login(username=ADMIN_USER['user'],
                          password=ADMIN_USER['password'])
        url = reverse('oppia_course_download', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        update_course_visibility(1, False, False)

    @pytest.mark.xfail(reason="works on local but not on github workflows")
    def test_draft_course_staff(self):
        update_course_visibility(1, True, False)
        self.client.login(username=STAFF_USER['user'],
                          password=STAFF_USER['password'])
        url = reverse('oppia_course_download', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'],
                         self.STR_EXPECTED_CONTENT_TYPE)
        update_course_visibility(1, False, False)

    def test_draft_course_teacher(self):
        update_course_visibility(1, True, False)
        self.client.login(username=TEACHER_USER['user'],
                          password=TEACHER_USER['password'])
        url = reverse('oppia_course_download', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        update_course_visibility(1, False, False)

    def test_draft_course_normal(self):
        update_course_visibility(1, True, False)
        self.client.login(username=NORMAL_USER['user'],
                          password=NORMAL_USER['password'])
        url = reverse('oppia_course_download', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        update_course_visibility(1, False, False)

    def test_archived_course_admin(self):
        update_course_visibility(1, False, True)
        self.client.login(username=ADMIN_USER['user'],
                          password=ADMIN_USER['password'])
        url = reverse('oppia_course_download', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        update_course_visibility(1, False, False)

    def test_archived_course_staff(self):
        update_course_visibility(1, False, True)
        self.client.login(username=STAFF_USER['user'],
                          password=STAFF_USER['password'])
        url = reverse('oppia_course_download', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        update_course_visibility(1, False, False)

    def test_archived_course_teacher(self):
        update_course_visibility(1, False, True)
        self.client.login(username=TEACHER_USER['user'],
                          password=TEACHER_USER['password'])
        url = reverse('oppia_course_download', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        update_course_visibility(1, False, False)

    def test_archived_course_normal(self):
        update_course_visibility(1, False, True)
        self.client.login(username=NORMAL_USER['user'],
                          password=NORMAL_USER['password'])
        url = reverse('oppia_course_download', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        update_course_visibility(1, False, False)

    # Course does not exist
    def test_dne_course_admin(self):
        self.client.login(username=ADMIN_USER['user'],
                          password=ADMIN_USER['password'])
        url = reverse('oppia_course_download', args=[123])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_dne_course_staff(self):
        self.client.login(username=STAFF_USER['user'],
                          password=STAFF_USER['password'])
        url = reverse('oppia_course_download', args=[123])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_dne_course_teacher(self):
        self.client.login(username=TEACHER_USER['user'],
                          password=TEACHER_USER['password'])
        url = reverse('oppia_course_download', args=[123])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_dne_course_normal(self):
        self.client.login(username=NORMAL_USER['user'],
                          password=NORMAL_USER['password'])
        url = reverse('oppia_course_download', args=[123])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
