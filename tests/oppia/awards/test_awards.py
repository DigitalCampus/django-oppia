from oppia.awards import courses_completed
from oppia.test import OppiaTestCase


class AwardsNoBadgesTest(OppiaTestCase):

    def test_badges_not_loaded(self):
        result = courses_completed(0)
        self.assertFalse(result)