from django.urls import reverse
from oppia.test import OppiaTestCase
from settings import constants
from settings.models import SettingProperties


class RegisterViewTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_course_permissions.json']

    def setUp(self):
        super(RegisterViewTest, self).setUp()
        self.url = reverse('profile:register')
        self.thanks_url = reverse('profile:register_thanks')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'common/form/form.html')
        self.assertEqual(200, response.status_code)

    # check form not filled
    def test_missing_fields(self):
        unfilled_form = {
            'username': 'new_username',
            'password': 'password'
        }
        res = self.client.post(self.url, data=unfilled_form)
        self.assertFormError(res,
                             'form',
                             'password_again',
                             'Please enter your password again.')

    # check passwords dont match
    def test_password_not_match(self):
        filled_form = {
            'username': 'new_username',
            'email': 'newusername@email.com',
            'password': 'password',
            'password_again': 'otherpass',
            'first_name': 'Test name',
            'last_name': 'Last name'
        }
        res = self.client.post(self.url, data=filled_form)
        self.assertFormError(res,
                             'form',
                             None,
                             errors='Passwords do not match.')

    # check user already exists
    def test_existing_user(self):
        filled_form = {
            'username': 'demo',
            'email': 'newusername@email.com',
            'password': 'password',
            'password_again': 'password',
            'first_name': 'Test name',
            'last_name': 'Last name'
        }
        res = self.client.post(self.url, data=filled_form)
        error_str = \
            'Username has already been registered, please select another.'
        self.assertFormError(res,
                             'form',
                             None,
                             errors=error_str)

    # check email already registered
    def test_existing_email(self):
        filled_form = {
            'username': 'new_username',
            'email': 'demo@me.com',
            'password': 'password',
            'password_again': 'password',
            'first_name': 'Test name',
            'last_name': 'Last name'
        }
        res = self.client.post(self.url, data=filled_form)
        self.assertFormError(res,
                             'form',
                             None,
                             errors='Email has already been registered')

    # check correct registration
    def test_correct_register(self):
        filled_form = {
            'username': 'new_username',
            'email': 'newusername@email.com',
            'password': 'password',
            'password_again': 'password',
            'first_name': 'Test name',
            'last_name': 'Last name'
        }
        resp = self.client.post(self.url, data=filled_form)
        self.assertRedirects(resp, expected_url=self.thanks_url)

    def test_self_registration_disabled_cant_view(self):
        # turn off self registration
        SettingProperties.set_bool(constants.OPPIA_ALLOW_SELF_REGISTRATION,
                                   False)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

        # turn back on
        SettingProperties.set_bool(constants.OPPIA_ALLOW_SELF_REGISTRATION,
                                   True)

    def test_self_registration_disabled_cant_post(self):
        # turn off self registration
        SettingProperties.set_bool(constants.OPPIA_ALLOW_SELF_REGISTRATION,
                                   False)
        filled_form = {
            'username': 'new_username',
            'email': 'newusername@email.com',
            'password': 'password',
            'password_again': 'password',
            'first_name': 'Test name',
            'last_name': 'Last name'
        }
        response = self.client.post(self.url, data=filled_form)
        self.assertEqual(response.status_code, 404)

        # turn back on
        SettingProperties.set_bool(constants.OPPIA_ALLOW_SELF_REGISTRATION,
                                   True)
