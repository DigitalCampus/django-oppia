
from oppia.test import OppiaTestCase
from gamification.forms import GamificationEventForm


class GamificationFormsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'default_gamification_events.json']

    # @TODO - complete this
    def test_gamification_event_form(self):
        GamificationEventForm()
