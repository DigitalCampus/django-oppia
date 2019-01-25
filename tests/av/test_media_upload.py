# tests/av/test_course_publish.py
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from tests.utils import *

from av.forms import UploadMediaForm

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
    '''    
    
    TODO - find a way to test this reliably with the mime types, see: 
    https://stackoverflow.com/questions/54366621/django-unit-testing-is-it-possible-to-specify-a-mime-type-for-file-upload
    
    def test_upload_template(self):
        
        media_file = open(self.media_file_path,'rb') 
        
        self.client.login(username=self.admin_user['user'], password=self.admin_user['password'])
        
        response = self.client.post(reverse('oppia_av_upload'), {'media_file': media_file })
        
        self.assertEqual(response.status_code, 200)
        
        media_file.close()
    
            
    def test_upload_form(self):
        
        media_file = open(self.media_file_path,'rb') 
        
        form_data = {'media_file': media_file}
        form = UploadMediaForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        media_file.close()
    '''