from django.conf import settings

from oppia.awards import courses_completed
from oppia.test import OppiaTestCase

from tests.oppia.awards.award_test_case import AwardsTestCase

      
class InvalidBadgeMethod(AwardsTestCase):

    def test_invalid_badge(self):
        settings.BADGE_AWARDING_METHOD = "invalid method"
        result = courses_completed(0)
        self.assertFalse(result)
