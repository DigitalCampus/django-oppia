
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.paginator import InvalidPage
from django.forms import ValidationError
from django.urls import reverse
from oppia.test import OppiaTestCase
from profile.models import UserProfile

from oppia.models import Badge, BadgeMethod
from settings.models import SettingProperties
from settings import constants


class OppiaViewsTest(OppiaTestCase):

    leaderboard_template = 'oppia/leaderboard.html'

    URL_INDEX = reverse('oppia:index')
    URL_SERVER = reverse('oppia:server')
    URL_MANAGER_INDEX = reverse('oppia:manager_index')
    URL_LEADERBOARD = reverse('oppia:leaderboard')
    
    def test_home(self):
        response = self.client.get(self.URL_INDEX)
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.post(reverse('profile:register'),
                                    {'username': 'demo2',
                                     'password': 'secret',
                                     'password_again': 'secret',
                                     'email': 'demo@demo.com',
                                     'first_name': 'demo',
                                     'last_name': 'user'})
        self.assertEqual(response.status_code, 302)

    def test_register_with_no_data(self):
        response = self.client.post(reverse('profile:register'), {})
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post(self.login_url,
                                    {'username': 'demo2',
                                     'password': 'secret'})
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get(reverse('oppia:about'))
        self.assertTemplateUsed(response, 'oppia/about.html')
        self.assertEqual(response.status_code, 200)

    def test_server(self):
        response = self.client.get(self.URL_SERVER)
        self.assertTemplateUsed(response, 'oppia/server.html')
        self.assertEqual(response['Content-Type'], "application/json")
        self.assertIsNotNone(response.json()['version'])
        self.assertIsNotNone(response.json()['name'])
        self.assertIsNotNone(response.json()['admin_email'])
        self.assertIsNotNone(response.json()['max_upload'])
        self.assertIsNotNone(response.json()['course_complete_badge_criteria'])
        self.assertIsNotNone(
            response.json()['course_complete_badge_criteria_percent'])
        self.assertEqual(response.status_code, 200)

    def test_server_update_badge_criteria(self):
        badge_method = BadgeMethod.objects.get(key="all_quizzes_plus_percent")
        badge = Badge.objects.get(ref='coursecompleted')
        badge.default_method = badge_method
        badge.save()
        response = self.client.get(self.URL_SERVER)
        self.assertEqual("all_quizzes_plus_percent",
                         response.json()['course_complete_badge_criteria'])
        
        badge_method = BadgeMethod.objects.get(key="all_activities")
        badge = Badge.objects.get(ref='coursecompleted')
        badge.default_method = badge_method
        badge.save()
        response = self.client.get(self.URL_SERVER)
        self.assertEqual("all_activities",
                         response.json()['course_complete_badge_criteria'])
    
    def test_server_update_badge_criteria_percent(self):
        SettingProperties.set_int(constants.OPPIA_BADGES_PERCENT_COMPLETED, 37)
        response = self.client.get(self.URL_SERVER)
        self.assertEqual(37,
            response.json()['course_complete_badge_criteria_percent'])
        
        SettingProperties.set_int(constants.OPPIA_BADGES_PERCENT_COMPLETED, 80)
        response = self.client.get(self.URL_SERVER)
        self.assertEqual(80,
            response.json()['course_complete_badge_criteria_percent'])
    '''
    homepage - post
    '''
    def test_home_admin_post_days(self):
        self.client.force_login(user=self.admin_user)
        data = {'start_date': '2019-12-01',
                'end_date': '2019-12-31',
                'interval': 'days'}
        response = self.client.post(self.URL_INDEX, data)
        self.assertEqual(200, response.status_code)

    def test_home_admin_post_months(self):
        self.client.force_login(user=self.admin_user)
        data = {'start_date': '2019-01-01',
                'end_date': '2019-12-31',
                'interval': 'months'}
        response = self.client.post(self.URL_INDEX, data)
        self.assertEqual(200, response.status_code)

    def test_home_admin_post_invalid_dates(self):
        self.client.force_login(user=self.admin_user)
        data = {'start_date': '2019-01',
                'end_date': '2019-12',
                'interval': 'months'}
        response = self.client.post(self.URL_INDEX, data)
        self.assertRaises(ValidationError)
        self.assertEqual(200, response.status_code)

    def test_home_manager_post_days(self):
        self.client.force_login(user=self.manager_user)
        data = {'start_date': '2019-12-01',
                'end_date': '2019-12-31',
                'interval': 'days'}
        response = self.client.post(self.URL_MANAGER_INDEX, data)
        self.assertEqual(200, response.status_code)

    def test_home_manager_post_months(self):
        self.client.force_login(user=self.manager_user)
        data = {'start_date': '2019-01-01',
                'end_date': '2019-12-31',
                'interval': 'months'}
        response = self.client.post(self.URL_MANAGER_INDEX, data)
        self.assertEqual(200, response.status_code)

    def test_home_manager_post_invalid_dates(self):
        self.client.force_login(user=self.manager_user)
        data = {'start_date': '2019-01',
                'end_date': '2019-12',
                'interval': 'months'}
        response = self.client.post(self.URL_MANAGER_INDEX, data)
        self.assertRaises(ValidationError)
        self.assertEqual(200, response.status_code)

    def test_home_teacher_get(self):
        self.client.force_login(user=self.teacher_user)
        response = self.client.get(reverse('oppia:teacher_index'))
        self.assertEqual(200, response.status_code)

    '''
    Leaderboard view
    '''
    def test_leaderboard_get(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(self.URL_LEADERBOARD)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.leaderboard_template)

    def test_leaderboard_get_page_1(self):
        self.client.force_login(user=self.admin_user)
        url = '%s?page=1' % self.URL_LEADERBOARD
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.leaderboard_template)

    def test_leaderboard_get_page_9999(self):
        self.client.force_login(user=self.admin_user)
        url = '%s?page=9999' % self.URL_LEADERBOARD
        response = self.client.get(url)
        self.assertRaises(InvalidPage)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.leaderboard_template)

    def test_leaderboard_get_page_abc(self):
        self.client.force_login(user=self.admin_user)
        url = '%s?page=abc' % self.URL_LEADERBOARD
        response = self.client.get(url)
        self.assertRaises(ValueError)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.leaderboard_template)

    def test_userprofile_created(self):
        user = User()
        user.username = 'noprofile'
        user.password = make_password('noprofile')
        user.save()
        self.client.force_login(user=user)

        start_count = UserProfile.objects.all().count()
        self.client.get(self.URL_INDEX)
        self.assertRaises(UserProfile.DoesNotExist)

        end_count = UserProfile.objects.all().count()
        self.assertEqual(start_count+1, end_count)
