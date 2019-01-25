# tests/av/test_course_publish.py

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from tests.utils import *

from av.forms import UploadMediaForm
from av.models import UploadedMedia

class MediaUploadResourceTest(TestCase):
    fixtures = ['user.json', 'oppia.json', 'quiz.json', 'permissions.json']
    
    course_file_path = './oppia/fixtures/reference_files/anc_course.zip' 
    media_file_path = './oppia/fixtures/reference_files/sample_video.m4v'
    
    def setUp(self):
        super(MediaUploadResourceTest, self).setUp()

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
        
        media_file_content = open(self.media_file_path,'rb') 
        media_file = SimpleUploadedFile(media_file_content.name, media_file_content.read(), content_type="video/m4v")
        
        self.client.login(username=self.admin_user['user'], password=self.admin_user['password'])
        response = self.client.post(reverse('oppia_av_upload'), {'media_file': media_file })
        self.assertRedirects(response, reverse('oppia_av_upload_success', args=[1]), 302, 200)
        
        media_file_content.close()
    
        
        