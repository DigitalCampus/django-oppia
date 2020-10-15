
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.paginator import InvalidPage
from django.forms import ValidationError
from django.urls import reverse
from oppia.test import OppiaTestCase
from profile.models import UserProfile


class OppiaViewsTest(OppiaTestCase):

    leaderboard_template = 'oppia/leaderboard.html'

    def test_home(self):
        response = self.client.get(reverse('oppia:index'))
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
        response = self.client.get(reverse('oppia:server'))
        self.assertTemplateUsed(response, 'oppia/server.html')
        self.assertEqual(response['Content-Type'], "application/json")
        response.json()
        self.assertIsNotNone(response.json()['version'])
        self.assertIsNotNone(response.json()['name'])
        self.assertIsNotNone(response.json()['admin_email'])
        self.assertIsNotNone(response.json()['max_upload'])
        # check it can load as json object
        self.assertEqual(response.status_code, 200)

    '''
    homepage - post
    '''
    def test_home_post_days(self):
        self.client.force_login(user=self.admin_user)
        data = {'start_date': '2019-12-01',
                'end_date': '2019-12-31',
                'interval': 'days'}
        response = self.client.post(reverse('oppia:index'), data)
        self.assertEqual(200, response.status_code)

    def test_home_post_months(self):
        self.client.force_login(user=self.admin_user)
        data = {'start_date': '2019-01-01',
                'end_date': '2019-12-31',
                'interval': 'months'}
        response = self.client.post(reverse('oppia:index'), data)
        self.assertEqual(200, response.status_code)

    def test_home_post_invalid_dates(self):
        self.client.force_login(user=self.admin_user)
        data = {'start_date': '2019-01',
                'end_date': '2019-12',
                'interval': 'months'}
        response = self.client.post(reverse('oppia:index'), data)
        self.assertRaises(ValidationError)
        self.assertEqual(200, response.status_code)

    '''
    Leaderboard view
    '''
    def test_leaderboard_get(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse('oppia:leaderboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.leaderboard_template)

    def test_leaderboard_get_page_1(self):
        self.client.force_login(user=self.admin_user)
        url = '%s?page=1' % reverse('oppia:leaderboard')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.leaderboard_template)

    def test_leaderboard_get_page_9999(self):
        self.client.force_login(user=self.admin_user)
        url = '%s?page=9999' % reverse('oppia:leaderboard')
        response = self.client.get(url)
        self.assertRaises(InvalidPage)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.leaderboard_template)

    def test_leaderboard_get_page_abc(self):
        self.client.force_login(user=self.admin_user)
        url = '%s?page=abc' % reverse('oppia:leaderboard')
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
        self.client.get(reverse('oppia:index'))
        self.assertRaises(UserProfile.DoesNotExist)

        end_count = UserProfile.objects.all().count()
        self.assertEqual(start_count+1, end_count)
