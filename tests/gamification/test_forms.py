from django.urls import reverse
from oppia.test import OppiaTestCase
from gamification.forms import GamificationEventForm


class GamificationFormsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'default_gamification_events.json']

    def test_gamification_event_form_post(self):
        data = {
            'events-TOTAL_FORMS': 0,
            'events-INITIAL_FORMS': 0,
            'events-MIN_NUM_FORMS': 0,
            'events-MAX_NUM_FORMS': 1000
            }
        url = reverse('oppia_gamification_edit_course', args=[1])

        self.client.force_login(user=self.admin_user)
        response = self.client.post(url, data)
        self.assertEqual(200, response.status_code)
