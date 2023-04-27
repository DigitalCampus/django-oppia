import csv
import io

from django.urls import reverse
from oppia.test import OppiaTestCase


class ExportUsersViewsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json',
                'tests/test_customfields.json']

    STR_EXPECTED_CONTENT_TYPE = 'text/csv'
    STR_URL = 'profile:users_list'

    def test_permissions(self):
        for user in [self.normal_user,
                     self.teacher_user]:
            self.client.force_login(user)
            response = self.client.get(reverse(self.STR_URL) + "?export=csv&username=&first_name=&last_name=&email=" +
                                       "&is_active=&is_staff=&start_date=&end_date=&userprofilecustomfield_test=")
            self.assertEqual(403, response.status_code)

    def test_download_all_users_all_data(self):
        for user in [self.admin_user,
                     self.staff_user]:
            self.client.force_login(user)
            response = self.client.get(reverse(self.STR_URL) + "?export=csv&username=&first_name=&last_name=" +
                                       "&email=&is_active=&is_staff=&start_date=&end_date=" +
                                       "&userprofilecustomfield_test=")
            self.assertEqual(200, response.status_code)
            self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
            csv_file = csv.DictReader(io.StringIO(response.content.decode()))
            self.assertEqual(6, len(list(csv_file)))

    def test_download_filtered_by_registration_date_all_data(self):
        for user in [self.admin_user,
                     self.staff_user]:
            self.client.force_login(user)
            response = self.client.get(reverse(self.STR_URL) + "?export=csv&username=&first_name=&last_name=&email=" +
                                       "&is_active=&is_staff=&start_date=2022-01-01&end_date=2022-12-31" +
                                       "&userprofilecustomfield_test=")
            self.assertEqual(200, response.status_code)
            self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
            csv_file = csv.DictReader(io.StringIO(response.content.decode()))
            self.assertEqual(0, len(list(csv_file)))

    def test_download_all_users_username_only(self):
        for user in [self.admin_user,
                     self.staff_user]:
            self.client.force_login(user)
            response = self.client.get(reverse(self.STR_URL) + "?export=csv&username=&first_name=&last_name=&email=" +
                                       "&is_active=&is_staff=&start_date=&end_date=&userprofilecustomfield_test=" +
                                       "&csv_fields%5B%5D=username")
            self.assertEqual(200, response.status_code)
            self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
            csv_file = csv.DictReader(io.StringIO(response.content.decode()))
            self.assertEqual(6, len(list(csv_file)))

    def test_download_all_users_invalid_field(self):
        for user in [self.admin_user,
                     self.staff_user]:
            self.client.force_login(user)
            response = self.client.get(reverse(self.STR_URL) + "?export=csv&username=&first_name=&last_name=&email=" +
                                       "&notafield=&is_staff=&start_date=&end_date=&userprofilecustomfield_test=" +
                                       "&userprofilecustomfield_notafield=&csv_fields%5B%5D=invalidnotafield")
            self.assertEqual(200, response.status_code)
            self.assertEqual(response['content-type'], self.STR_EXPECTED_CONTENT_TYPE)
            csv_file = csv.DictReader(io.StringIO(response.content.decode()))
            self.assertEqual(0, len(list(csv_file)))
