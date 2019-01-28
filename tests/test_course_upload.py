# tests/av/test_course_publish.py

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from tests.utils import *

from oppia.forms.upload import UploadCourseStep1Form, UploadCourseStep2Form

class CourseUploadTest(TestCase):
    fixtures = ['user.json', 'oppia.json', 'quiz.json', 'permissions.json']
    
    course_file_path = './oppia/fixtures/reference_files/anc_course.zip' 
    media_file_path = './oppia/fixtures/reference_files/sample_video.m4v'
    
    def setUp(self):
        super(CourseUploadTest, self).setUp()

        self.admin_user = {
            'user': 'admin',
            'password': 'password'
        }
        self.staff_user = {
            'user': 'staff',
            'password': 'password'
        }
        self.normal_user = {
            'user': 'demo',
            'password': 'password'
        }
        self.teacher_user = {
            'user': 'teacher',
            'password': 'password'
        }
    
    def test_upload_template(self):
        
        course_file = open(self.course_file_path,'rb') 
        
        self.client.login(username=self.admin_user['user'], password=self.admin_user['password'])
        response = self.client.post(reverse('oppia_upload'), {'course_file': course_file })        
        self.assertRedirects(response, reverse('oppia_upload2', args=[1]), 302, 200) # should be redirected to the update step 2 form
        
        course_file.close()
    