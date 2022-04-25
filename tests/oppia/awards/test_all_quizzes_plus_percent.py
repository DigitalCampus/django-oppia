import os

from tests.oppia.awards.award_test_case import AwardsTestCase


class AllQuizzesPlusPercentAwardsTest(AwardsTestCase):

    '''
    BADGE_AWARD_METHOD_QUIZZES_PLUS_PERCENT
    '''
    def setUp(self):
        super(AllQuizzesPlusPercentAwardsTest, self).setUp()
        self.set_badge_method('all_quizzes_plus_percent')

    # all quizzes no other acts
    def test_all_quizzes_no_acts(self):
        file = os.path.join('all_quizzes_plus_percent', 'tracker_all_quiz_no_acts.json')
        self.load_trackers(file, 7)
        self.assert_points_and_awards(0, 0)

    # some quizzes no other acts
    def test_some_quizzes_no_acts(self):
        file = os.path.join('all_quizzes_plus_percent', 'tracker_some_quiz_no_acts.json')
        self.load_trackers(file, 7)
        self.assert_points_and_awards(0, 0)

    # no quizzes no other acts
    def test_no_quizzes_no_acts(self):
        file = os.path.join('all_quizzes_plus_percent', 'tracker_no_quiz_no_acts.json')
        self.load_trackers(file, 7)
        self.assert_points_and_awards(0, 0)

    # all quizzes 50% other acts
    def test_all_quizzes_50pc_acts(self):
        file = os.path.join('all_quizzes_plus_percent', 'tracker_all_quiz_50pc_acts.json')
        self.load_trackers(file, 7)
        self.assert_points_and_awards(0, 0)

    # some quizzes 50% other acts
    def test_some_quizzes_50pc_acts(self):
        file = os.path.join('all_quizzes_plus_percent', 'tracker_some_quiz_50pc_acts.json')
        self.load_trackers(file, 7)
        self.assert_points_and_awards(0, 0)

    # no quizzes 50% other acts
    def test_no_quizzes_50pc_acts(self):
        file = os.path.join('all_quizzes_plus_percent', 'tracker_no_quiz_50pc_acts.json')
        self.load_trackers(file, 7)
        self.assert_points_and_awards(0, 0)

    # all quizzes 80% other acts
    def test_all_quizzes_80pc_acts(self):
        file = os.path.join('all_quizzes_plus_percent', 'tracker_all_quiz_80pc_acts.json')
        self.load_trackers(file, 8)
        self.assert_points_and_awards(1, 1)

    # some quizzes 80% other acts
    def test_some_quizzes_80pc_acts(self):
        file = os.path.join('all_quizzes_plus_percent', 'tracker_some_quiz_80pc_acts.json')
        self.load_trackers(file, 8)
        self.assert_points_and_awards(0, 0)

    # no quizzes 80% other acts
    def test_no_quizzes_80pc_acts(self):
        file = os.path.join('all_quizzes_plus_percent', 'tracker_no_quiz_80pc_acts.json')
        self.load_trackers(file, 8)
        self.assert_points_and_awards(0, 0)

    # duplicate badges
    def test_all_quizzes_80pc_acts_duplicate_awards(self):
        file = os.path.join('all_quizzes_plus_percent', 'tracker_all_quiz_80pc_acts.json')
        self.load_trackers(file, 8)
        self.assert_points_and_awards(1, 1)
        self.assert_points_and_awards(0, 0, 24)
        self.assert_points_and_awards(0, 0, 0)
