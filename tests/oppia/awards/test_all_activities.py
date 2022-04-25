import os

from tests.oppia.awards.award_test_case import AwardsTestCase


class AllActivitiesAwardsTest(AwardsTestCase):

    def setUp(self):
        super(AllActivitiesAwardsTest, self).setUp()
        self.set_badge_method('all_activities')

    '''
    BADGE_AWARD_METHOD_ALL_ACTIVITIES
    '''
    # all activities completed and passed
    def test_all_acts_all_complete(self):
        file = os.path.join('all_activities', 'tracker_all_acts_all_complete.json')
        self.load_trackers(file, 8)
        self.assert_points_and_awards(1, 1)

    # all activities attempted, but not all complete
    def test_all_acts_some_complete(self):
        file = os.path.join('all_activities', 'tracker_all_acts_some_complete.json')
        self.load_trackers(file, 7)
        self.assert_points_and_awards(0, 0)

    # not all activities attempted
    def test_all_acts_some_attempted(self):
        file = os.path.join('all_activities', 'tracker_all_acts_some_attempted.json')
        self.load_trackers(file, 5)
        self.assert_points_and_awards(0, 0)

    # no activities completed
    def test_all_acts_none_completed(self):
        file = os.path.join('all_activities', 'tracker_all_attempted_none_completed.json')
        self.load_trackers(file, 6)
        self.assert_points_and_awards(0, 0)

    # check badge cannot be awarded twice
    def test_all_acts_duplicate_awards(self):
        file = os.path.join('all_activities', 'tracker_all_acts_all_complete.json')
        self.load_trackers(file, 8)
        self.assert_points_and_awards(1, 1)
        self.assert_points_and_awards(0, 0, 24)
        self.assert_points_and_awards(0, 0, 0)
