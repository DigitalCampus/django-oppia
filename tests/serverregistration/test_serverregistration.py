
from django.core.exceptions import PermissionDenied
from django.core.paginator import InvalidPage
from django.forms import ValidationError
from django.urls import reverse

from oppia.test import OppiaTestCase
from settings import constants
from settings.models import SettingProperties

class OppiaActivityViewsTest(OppiaTestCase):

    url_register_page = reverse('serverregistration:register')
    url_thanks_page = reverse('serverregistration:thanks')
    STR_REGISTER_TEMPLATE = 'serverregistration/register.html'

    STR_MY_SITE = 'https://mysite.com'
    STR_MY_EMAIL = 'my@email.com'
    
    # only staff/admin can access page
    def test_server_reg_admin(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(self.url_register_page)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.STR_REGISTER_TEMPLATE)

    def test_server_reg_staff(self):
        self.client.force_login(user=self.staff_user)
        response = self.client.get(self.url_register_page)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.STR_REGISTER_TEMPLATE)
        
    def test_server_reg_teacher(self):
        self.client.force_login(user=self.teacher_user)
        response = self.client.get(self.url_register_page)
        self.assertEqual(302, response.status_code)
        
    def test_server_reg_user(self):
        self.client.force_login(user=self.normal_user)
        response = self.client.get(self.url_register_page)
        self.assertEqual(302, response.status_code)
        
    # test post
    def test_post_all_fields(self):
        data = {'server_url': self.STR_MY_SITE,
                'include_no_courses': True,
                'include_no_users': True,
                 'email_notifications': True,
                 'notif_email_address': self.STR_MY_EMAIL}
        self.client.force_login(user=self.admin_user)
        response = self.client.post(self.url_register_page, data)
        self.assertRedirects(response,
                             self.url_thanks_page,
                             302,
                             200)
        
        # check data saved correctly
        self.assertEqual(self.STR_MY_SITE,
                         SettingProperties.get_property(
                             constants.OPPIA_HOSTNAME, ''))
        self.assertTrue(SettingProperties.get_property(
                             constants.OPPIA_SERVER_REGISTER_NO_COURSES, False))
        self.assertTrue(SettingProperties.get_property(
                             constants.OPPIA_SERVER_REGISTER_NO_USERS, False))
        self.assertTrue(SettingProperties.get_property(
                             constants.OPPIA_SERVER_REGISTER_EMAIL_NOTIF, False))
        self.assertEqual(self.STR_MY_EMAIL,
                         SettingProperties.get_property(
                             constants.OPPIA_SERVER_REGISTER_NOTIF_EMAIL_ADDRESS, ''))
        
    def test_post_change_fields(self):
        initial_data = {'server_url': self.STR_MY_SITE,
                'include_no_courses': True,
                'include_no_users': True,
                 'email_notifications': True,
                 'notif_email_address': self.STR_MY_EMAIL}
        self.client.force_login(user=self.admin_user)
        response = self.client.post(self.url_register_page, initial_data)
        self.assertRedirects(response,
                             self.url_thanks_page,
                             302,
                             200)
        
        changed_data = {'server_url': 'https://myothersite.com',
                'include_no_courses': False,
                'include_no_users': False,
                 'email_notifications': False,
                 'notif_email_address': 'myother@email.com'}
        self.client.force_login(user=self.admin_user)
        response = self.client.post(self.url_register_page, changed_data)
        self.assertRedirects(response,
                             self.url_thanks_page,
                             302,
                             200)
        
        # check data saved correctly
        self.assertEqual('https://myothersite.com',
                         SettingProperties.get_property(
                             constants.OPPIA_HOSTNAME, ''))
        self.assertFalse(SettingProperties.get_property(
                             constants.OPPIA_SERVER_REGISTER_NO_COURSES, False))
        self.assertFalse(SettingProperties.get_property(
                             constants.OPPIA_SERVER_REGISTER_NO_USERS, False))
        self.assertFalse(SettingProperties.get_property(
                             constants.OPPIA_SERVER_REGISTER_EMAIL_NOTIF, False))
        self.assertEqual('myother@email.com',
                         SettingProperties.get_property(
                             constants.OPPIA_SERVER_REGISTER_NOTIF_EMAIL_ADDRESS, ''))
