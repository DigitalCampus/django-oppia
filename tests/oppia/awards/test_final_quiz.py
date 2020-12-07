from django.conf import settings

from oppia.models import Tracker

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
        self.load_trackers(
            'final_quiz/tracker_final_quiz_passed.json', 1)
        self.assert_points_and_awards(1, 1)

    # no activities completed
    def test_final_quiz_none_completed(self):
        self.load_trackers(
            'final_quiz/tracker_all_attempted_none_completed.json', 6)
        self.assert_points_and_awards(0, 0)

    # some other activities completed but not final quiz
    def test_final_quiz_some_completed(self):
        self.load_trackers(
            'final_quiz/tracker_final_quiz_some_complete.json', 5)
        self.assert_points_and_awards(0, 0)

    # final quiz attempted but not passed
    def test_final_quiz_attempted(self):
        self.load_trackers(
            'final_quiz/tracker_final_quiz_attempted.json', 6)
        self.assert_points_and_awards(0, 0)

    # check badge cannot be awarded twice
    def test_final_quiz_duplicate_awards(self):
        self.load_trackers(
            'final_quiz/tracker_final_quiz_passed.json', 1)
        self.assert_points_and_awards(1, 1)
        self.assert_points_and_awards(0, 0, 24)
        self.assert_points_and_awards(0, 0, 0)
