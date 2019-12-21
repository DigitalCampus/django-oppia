from oppia.test import OppiaTestCase
from django.urls import reverse

                            
class ContentViewsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'default_gamification_events.json',
                'tests/test_tracker.json']

    def setUp(self):
        super(ContentViewsTest, self).setUp()
        self.media_embed_helper_url = reverse('oppia_media_embed_helper')
        self.video_embed_helper_url = reverse('oppia_video_embed_helper')
        
    # GET media embed helper
    def test_media_embed_helper_get_admin(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.media_embed_helper_url)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(self.video_embed_helper_url)
        self.assertEqual(response.status_code, 200)

    def test_media_embed_helper_get_staff(self):
        self.client.force_login(self.staff_user)
        response = self.client.get(self.media_embed_helper_url)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(self.video_embed_helper_url)
        self.assertEqual(response.status_code, 200)

    def test_media_embed_helper_get_teacher(self):
        self.client.force_login(self.teacher_user)
        response = self.client.get(self.media_embed_helper_url)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(self.video_embed_helper_url)
        self.assertEqual(response.status_code, 200)  

    def test_media_embed_helper_get_normal(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(self.media_embed_helper_url)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(self.video_embed_helper_url)
        self.assertEqual(response.status_code, 200)

    def test_media_embed_helper_get_anon(self):
        self.client.logout()
        response = self.client.get(self.media_embed_helper_url)
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(self.video_embed_helper_url)
        self.assertEqual(response.status_code, 200)   
    # @TODO POST media embed helper
    # @TODO process_media_file
    # @TODO check_media_link
    # @TODO get_length
    # @TODO generate_media_screenshots
    # @TODO can_execute
    # @TODO md5_checksum