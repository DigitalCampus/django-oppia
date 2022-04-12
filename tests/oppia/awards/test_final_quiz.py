import os

from tests.oppia.awards.award_test_case import AwardsTestCase


class FinalQuizAwardsTest(AwardsTestCase):

    '''
    BADGE_AWARD_METHOD_FINAL_QUIZ
    '''
    def setUp(self):
        super(FinalQuizAwardsTest, self).setUp()
        self.set_badge_method('final_quiz')

    # final quiz attempted and passed
    def test_final_quiz_passed(self):
        file = os.path.join('final_quiz', 'tracker_final_quiz_passed.json')
        self.load_trackers(file, 1)
        self.assert_points_and_awards(1, 1)

    # no activities completed
    def test_final_quiz_none_completed(self):
        file = os.path.join('final_quiz', 'tracker_all_attempted_none_completed.json')
        self.load_trackers(file, 6)
        self.assert_points_and_awards(0, 0)

    # some other activities completed but not final quiz
    def test_final_quiz_some_completed(self):
        file = os.path.join('final_quiz', 'tracker_final_quiz_some_complete.json')
        self.load_trackers(file, 5)
        self.assert_points_and_awards(0, 0)

    # final quiz attempted but not passed
    def test_final_quiz_attempted(self):
        file = os.path.join('final_quiz', 'tracker_final_quiz_attempted.json')
        self.load_trackers(file, 6)
        self.assert_points_and_awards(0, 0)

    # check badge cannot be awarded twice
    def test_final_quiz_duplicate_awards(self):
        file = os.path.join('final_quiz', 'tracker_final_quiz_passed.json')
        self.load_trackers(file, 1)
        self.assert_points_and_awards(1, 1)
        self.assert_points_and_awards(0, 0, 24)
        self.assert_points_and_awards(0, 0, 0)
