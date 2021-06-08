from django.urls import reverse
from oppia.test import OppiaTestCase


class ManageViewsTest(OppiaTestCase):

    def test_delete_account_get(self):
        url = reverse('profile:delete', args=[self.normal_user.id])
        self.client.force_login(self.normal_user)
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'profile/delete_account.html')
