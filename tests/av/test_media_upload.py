# tests/av/test_course_publish.py

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from tests.utils import *

from av.forms import UploadMediaForm
from av.models import UploadedMedia

from tests.user_logins import *

class MediaUploadResourceTest(TestCase):
    fixtures = ['tests/test_user.json', 
                'tests/test_oppia.json', 
                'tests/test_quiz.json', 
                'tests/test_permissions.json']
    
    course_file_path = './oppia/fixtures/reference_files/anc_course.zip' 
    media_file_path = './oppia/fixtures/reference_files/sample_video.m4v'
    
    def setUp(self):
        super(MediaUploadResourceTest, self).setUp()
 

    def test_upload_template(self):
        
        media_file_content = open(self.media_file_path,'rb') 
        media_file = SimpleUploadedFile(media_file_content.name, media_file_content.read(), content_type="video/m4v")
        
        self.client.login(username=ADMIN_USER['user'], password=ADMIN_USER['password'])
        response = self.client.post(reverse('oppia_av_upload'), {'media_file': media_file })
        self.assertRedirects(response, reverse('oppia_av_upload_success', args=[1]), 302, 200)
        
        media_file_content.close()
    
        
        