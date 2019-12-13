from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import TestCase

from tests.user_logins import ADMIN_USER, \
                              STAFF_USER, \
                              NORMAL_USER, \
                              TEACHER_USER
from tests.defaults import UNAUTHORISED_TEMPLATE


class UserUploadActivityViewTest(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']

    upload_user_file_valid = \
        './oppia/fixtures/reference_files/upload-user-file-valid.csv'

    def setUp(self):
        super(UserUploadActivityViewTest, self).setUp()
        self.template = 'profile/upload.html'
        self.url = reverse('profile_upload')

    def test_view_upload_permissions(self):

        allowed_users = [ADMIN_USER]
        disallowed_users = [STAFF_USER, TEACHER_USER, NORMAL_USER]

        for allowed_user in allowed_users:
            self.client.login(username=allowed_user['user'],
                              password=allowed_user['password'])
            response = self.client.get(self.url)
            self.assertTemplateUsed(response, self.template)
            self.assertEqual(response.status_code, 200)

        for disallowed_user in disallowed_users:
            self.client.login(username=disallowed_user['user'],
                              password=disallowed_user['password'])
            response = self.client.get(self.url)
            self.assertTemplateUsed(response, UNAUTHORISED_TEMPLATE)
            self.assertEqual(response.status_code, 403)

    
    def test_view_upload_valid_file(self):
        self.client.login(username=ADMIN_USER['user'],
                          password=ADMIN_USER['password'])

        with open(self.upload_user_file_valid, 'rb') as upload_user_file:
            upload_file = SimpleUploadedFile(upload_user_file.name,
                                             upload_user_file.read())

        user_count_start = User.objects.all().count()

        self.client.post(reverse('profile_upload'),
                                 {'upload_file': upload_file})

        user_count_end = User.objects.all().count()
        self.assertEqual(user_count_start+2, user_count_end)
    '''
    @TODO - complete the tests below
    def test_view_upload_invalid_file(self):
        
    def test_view_upload_no_password(self):
    
    def test_view_upload_with_password(self):
    '''
