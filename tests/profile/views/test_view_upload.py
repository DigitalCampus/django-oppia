import pytest

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from oppia.test import OppiaTransactionTestCase

from tests.defaults import UNAUTHORISED_TEMPLATE


class UserUploadActivityViewTest(OppiaTransactionTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']

    fixture_root = './oppia/fixtures/reference_files/'
    upload_user_file_valid = \
        fixture_root + 'upload-user-file-valid.csv'
    upload_user_file_duplicate_user = \
        fixture_root + 'upload-user-duplicate-user.csv'
    upload_user_file_invalid = \
        fixture_root + 'upload-user-file-invalid.csv'
    upload_user_file_valid_with_password = \
        fixture_root + 'upload-user-file-valid-with-password.csv'

    template = 'profile/upload.html'
    url = reverse('profile:upload')

    def setUp(self):
        super(UserUploadActivityViewTest, self).setUp()
        self.allowed_users = [self.admin_user]
        self.disallowed_users = [self.staff_user,
                                 self.teacher_user,
                                 self.normal_user]

    def test_view_upload_permissions_get(self):

        for allowed_user in self.allowed_users:
            self.client.force_login(user=allowed_user)
            response = self.client.get(self.url)
            self.assertTemplateUsed(response, self.template)
            self.assertEqual(response.status_code, 200)

        for disallowed_user in self.disallowed_users:
            self.client.force_login(user=disallowed_user)
            response = self.client.get(self.url)
            self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)
            self.assertEqual(response.status_code, 403)

    def test_view_upload_permissions_post(self):

        for allowed_user in self.allowed_users:
            self.client.force_login(user=allowed_user)
            response = self.client.post(self.url)
            self.assertTemplateUsed(response, self.template)
            self.assertEqual(response.status_code, 200)

        for disallowed_user in self.disallowed_users:
            self.client.force_login(user=disallowed_user)
            response = self.client.post(self.url)
            self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)
            self.assertEqual(response.status_code, 403)

    def test_view_upload_valid_file(self):
        self.client.force_login(user=self.admin_user)

        with open(self.upload_user_file_valid, 'rb') as upload_user_file:
            upload_file = SimpleUploadedFile(upload_user_file.name,
                                             upload_user_file.read())

        user_count_start = User.objects.all().count()

        self.client.post(self.url, {'upload_file': upload_file})

        user_count_end = User.objects.all().count()
        self.assertEqual(user_count_start+2, user_count_end)

    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
    def test_view_upload_duplicate_user(self):
        self.client.force_login(user=self.admin_user)

        with open(self.upload_user_file_duplicate_user,
                  'rb') as upload_user_file:
            upload_file = SimpleUploadedFile(upload_user_file.name,
                                             upload_user_file.read())

        user_count_start = User.objects.all().count()

        self.client.post(self.url, {'upload_file': upload_file})

        user_count_end = User.objects.all().count()
        self.assertEqual(user_count_start+2, user_count_end)

    def test_view_upload_invalid_file(self):
        self.client.force_login(user=self.admin_user)

        with open(self.upload_user_file_invalid, 'rb') as upload_user_file:
            upload_file = SimpleUploadedFile(upload_user_file.name,
                                             upload_user_file.read())

        user_count_start = User.objects.all().count()

        self.client.post(self.url, {'upload_file': upload_file})

        user_count_end = User.objects.all().count()
        self.assertEqual(user_count_start, user_count_end)

    def test_view_upload_with_password(self):
        self.client.force_login(user=self.admin_user)

        with open(self.upload_user_file_valid_with_password, 'rb') \
                as upload_user_file:
            upload_file = SimpleUploadedFile(upload_user_file.name,
                                             upload_user_file.read())

        user_count_start = User.objects.all().count()

        self.client.post(self.url, {'upload_file': upload_file})

        user_count_end = User.objects.all().count()
        self.assertEqual(user_count_start+2, user_count_end)

        # check can login with new password
        self.client.logout()
        self.client.login(username='user100', password='password100')
        self.client.get(reverse('oppia:index'))
        self.assertTemplateUsed('profile/user-scorecard.htm')
