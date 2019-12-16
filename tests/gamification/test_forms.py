
from django.test import TestCase
from gamification.forms import GamificationEventForm

class GamificationFormsTest(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'default_gamification_events.json']

    def setUp(self):
        super(GamificationFormsTest, self).setUp()

    # @TODO - complete this
    def test_gamification_event_form(self):
        GamificationEventForm()