# tests/api/test_course_publish.py
from django import forms
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User


class MediaPublishResourceTest(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']

    def setUp(self):
        self.client = Client()
        self.url = '/api/media/'
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

        video_file = open(self.video_file_path, 'rb')

        # no username
        response = self.client.post(self.url,
                                    {'password': 'secret',
                                     'media_file': video_file})
        self.assertRaises(forms.ValidationError)
        self.assertEqual(response.status_code, 400)

        # no password
        response = self.client.post(self.url,
                                    {'username': 'demo',
                                     'media_file': video_file})
        self.assertEqual(response.status_code, 400)

        # shouldn't be strictly necessary to close the file,
        # but avoids ResourceWarnings about unclosed files
        video_file.close()

    # check authentication check working correctly
    def test_authentication(self):

        video_file = open(self.video_file_path, 'rb')
        # incorrect username
        response = self.client.post(self.url,
                                    {'username': 'demouser',
                                     'password': 'password',
                                     'media_file': video_file})
        self.assertEqual(response.status_code, 401)

        # incorrect password
        response = self.client.post(self.url,
                                    {'username': 'demo',
                                     'password': 'wrong_password',
                                     'media_file': video_file})
        self.assertEqual(response.status_code, 401)

        video_file.close()
        # shouldn't be strictly necessary to close the file,
        # but avoids ResourceWarnings about unclosed files

    # test is user has correct permissions or not to upload
    def test_permissions(self):
        # set to inactive user
        user = User.objects.get(username='demo')
        user.is_active = False
        user.save()

        video_file = open(self.video_file_path, 'rb')

        response = self.client.post(self.url,
                                    {'username': 'demo',
                                     'password': 'password',
                                     'media_file': video_file})
        self.assertEqual(response.status_code, 401)

        video_file.close()
        # shouldn't be strictly necessary to close the file,
        # but avoids ResourceWarnings about unclosed files

        # set back to active user
        user.is_active = True
        user.save()

    # check upload works for all users
    def test_upload(self):

        '''
        TODO - the test framework seems to only recognise the file as
        'application/octet-stream', so upload ways fails as incorrect
        mime-type is found

        # normal user
        response = self.client.post(self.url,{'username': 'demo',
                                              'password': 'password',
                                              'media_file': video_file })
        self.assertEqual(response.status_code, 201)

        # teacher
        response = self.client.post(self.url, {'username': 'teacher',
                                               'password': 'password',
                                               'media_file': video_file })
        self.assertEqual(response.status_code, 201)

        # staff
        response = self.client.post(self.url, {'username': 'staff',
                                               'password': 'password',
                                               'media_file': video_file })
        self.assertEqual(response.status_code, 201)

        # admin
        response = self.client.post(self.url, {'username': 'admin',
                                               'password': 'password',
                                               'media_file': video_file })
        self.assertEqual(response.status_code, 201)
        '''
        pass

    # test file type
    def test_filetype(self):

        course_file = open(self.course_file_path, 'rb')

        # send zip file
        response = self.client.post(self.url,
                                    {'username': 'demo',
                                     'password': 'password',
                                     'media_file': course_file})
        self.assertEqual(response.status_code, 400)

        # shouldn't be strictly necessary to close the file,
        # but avoids ResourceWarnings about unclosed files
        course_file.close()
