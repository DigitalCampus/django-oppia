import os
import unittest
import pytest

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APITestCase

from tests.api.v3 import utils


class MediaAPITests(APITestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_av_uploadedmedia.json',
                'tests/test_course_permissions.json']

    url = '/api/v3/media/'
    valid_digest = '/api/v3/media/3f2d7d54e969e303901ba5a177bd2334'
    invalid_digest = '/api/v3/media/123456789'
    course_file_path = os.path.join(settings.TEST_RESOURCES, 'ncd1_test_course.zip')
    video_file_path = os.path.join(settings.TEST_RESOURCES, 'sample_video.m4v')

    # test all params have been sent
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_required_params(self):

        # no username
        with open(self.video_file_path, 'rb') as video_file:
            data = {'password': 'secret', 'media_file': video_file}
            response = self.client.post(self.url, data=data, content_type="application/json")

        self.assertEqual(response.status_code, utils.HTTP_BAD_REQUEST)

        # no password
        with open(self.video_file_path, 'rb') as video_file:
            data = {'username': 'demo', 'media_file': video_file}
            response = self.client.post(self.url, data=data, content_type="application/json")

        self.assertEqual(response.status_code, utils.HTTP_BAD_REQUEST)

    # check authentication check working correctly
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_authentication(self):

        # incorrect username
        with open(self.video_file_path, 'rb') as video_file:
            data = {'username': 'demouser', 'password': 'password', 'media_file': video_file}
            response = self.client.post(self.url, data=data, content_type="application/json")

        self.assertEqual(response.status_code, utils.HTTP_UNAUTHORIZED)

        # incorrect password
        with open(self.video_file_path, 'rb') as video_file:
            data = {'username': 'demo', 'password': 'wrong_password', 'media_file': video_file}
            response = self.client.post(self.url, data=data, content_type="application/json")

        self.assertEqual(response.status_code, utils.HTTP_UNAUTHORIZED)

    # test is user has correct permissions or not to upload
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_permissions(self):
        # set to inactive user
        user = utils.get_normal_user()
        user.is_active = False
        user.save()

        with open(self.video_file_path, 'rb') as video_file:
            data = {'username': 'demo', 'password': 'password', 'media_file': video_file}
            response = self.client.post(self.url, data=data, content_type="application/json")

        self.assertEqual(response.status_code, utils.HTTP_UNAUTHORIZED)

        # set back to active user
        user.is_active = True
        user.save()

    # check upload works for all users
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_upload_user(self):

        # normal user
        with open(self.video_file_path, 'rb') as video_file:
            upload_file = SimpleUploadedFile(video_file.name,
                                             video_file.read(),
                                             content_type='video/m4v')
            data = {'username': 'demo', 'password': 'password', 'media_file': upload_file}
            response = self.client.post(self.url, data=data, content_type="application/json")

        self.assertEqual(response.status_code, utils.HTTP_CREATED)
        response_data = response.json()

        self.assertTrue('digest' in response_data)
        self.assertTrue('length' in response_data)
        self.assertTrue('filesize' in response_data)
        self.assertTrue('download_url' in response_data)

        self.assertEqual("5c414654ad2bd2bc1ea9819435e1f193", response_data['digest'])
        self.assertEqual(4, response_data['length'])
        self.assertEqual(496995, response_data['filesize'])
        self.assertTrue(response_data['download_url'].startswith("http://testserver/media/uploaded/"))
        self.assertTrue(response_data['download_url'].endswith(".m4v"))

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_upload_teacher(self):
        # teacher
        with open(self.video_file_path, 'rb') as video_file:
            upload_file = SimpleUploadedFile(video_file.name,
                                             video_file.read(),
                                             content_type='video/m4v')
            data = {'username': 'teacher', 'password': 'password', 'media_file': upload_file}
            response = self.client.post(self.url, data=data, content_type="application/json")

        self.assertEqual(response.status_code, utils.HTTP_CREATED)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_upload_staff(self):
        # staff
        with open(self.video_file_path, 'rb') as video_file:
            upload_file = SimpleUploadedFile(video_file.name,
                                             video_file.read(),
                                             content_type='video/m4v')
            data = {'username': 'staff', 'password': 'password', 'media_file': upload_file}
            response = self.client.post(self.url, data=data, content_type="application/json")

        self.assertEqual(response.status_code, utils.HTTP_CREATED)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_upload_admin(self):
        # admin
        with open(self.video_file_path, 'rb') as video_file:
            upload_file = SimpleUploadedFile(video_file.name,
                                             video_file.read(),
                                             content_type='video/m4v')
            data = {'username': 'admin', 'password': 'password', 'media_file': upload_file}
            response = self.client.post(self.url, data=data, content_type="application/json")

        self.assertEqual(response.status_code, utils.HTTP_CREATED)

    # test file type
    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_filetype(self):
        # send zip file
        with open(self.course_file_path, 'rb') as course_file:
            data = {'username': 'demo', 'password': 'password', 'media_file': course_file}
            response = self.client.post(self.url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, utils.HTTP_BAD_REQUEST)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_digest_valid(self):
        response = self.client.get(self.valid_digest)
        self.assertEqual(response.status_code, utils.HTTP_OK)
        json_data = response.json()

        self.assertEqual(json_data['digest'], "3f2d7d54e969e303901ba5a177bd2334")
        self.assertEqual(json_data['filesize'], 0)
        url = "http://testserver/media/uploaded/2018/02/MH1_Keyboard_480p.mp4"
        self.assertEqual(json_data['download_url'], url)
        self.assertEqual(json_data['length'], 170)
        self.assertEqual(json_data['title'], None)
        self.assertEqual(json_data['organisation'], None)
        self.assertEqual(json_data['license'], None)

    @unittest.expectedFailure
    @pytest.mark.xfail(reason="api endpoint not enabled")
    def test_digest_invalid(self):
        response = self.client.get(self.invalid_digest)
        self.assertEqual(response.status_code, utils.HTTP_NOT_FOUND)
