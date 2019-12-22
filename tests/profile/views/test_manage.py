from django.urls import reverse
from oppia.test import OppiaTestCase
from profile.forms import DeleteAccountForm


class ManageViewsTest(OppiaTestCase):
    
    def test_delete_account_get(self):
        url = reverse('profile_delete_account')
        self.client.force_login(self.normal_user)
        self.client.get(url)
        self.assertTemplateUsed('profile/delete_account.html')