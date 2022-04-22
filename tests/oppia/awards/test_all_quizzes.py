import os

from tests.oppia.awards.award_test_case import AwardsTestCase


class AllQuizzesAwardsTest(AwardsTestCase):

    '''
    BADGE_AWARD_METHOD_ALL_QUIZZES
    '''
    def setUp(self):
        super(AllQuizzesAwardsTest, self).setUp()
        self.set_badge_method('all_quizzes')

    # both quizzes passed
    def test_all_quiz_passed(self):
        file = os.path.join('all_quizzes', 'tracker_all_quizzes_complete.json')
        self.load_trackers(file, 2)
        self.assert_points_and_awards(1, 1)

    # no activities completed
    def test_all_quiz_none_complete(self):
        file = os.path.join('all_quizzes', 'tracker_all_quizzes_none_complete.json')
        self.load_trackers(file, 6)
        self.assert_points_and_awards(0, 0)

    # some other activities completed but not quizzes
    def test_all_quiz_some_activities_complete(self):
        file = os.path.join('all_quizzes', 'tracker_all_quizzes_some_complete.json')
        self.load_trackers(file, 6)
        self.assert_points_and_awards(0, 0)

    # one quiz passed and the other not attempted
    def test_all_quiz_some_complete(self):
        file = os.path.join('all_quizzes', 'tracker_all_quizzes_one_passed.json')
        self.load_trackers(file,  5)
        self.assert_points_and_awards(0, 0)

    # both quizzes attempted but not passed
    def test_all_quiz_attempted_only(self):
        file = os.path.join('all_quizzes', 'tracker_all_quizzes_attempted_only.json')
        self.load_trackers(file, 6)
        self.assert_points_and_awards(0, 0)

    # check badge cannot be awarded twice
    def test_all_quiz_duplicate_awards(self):
        file = os.path.join('all_quizzes', 'tracker_all_quizzes_complete.json')
        self.load_trackers(file, 2)
        self.assert_points_and_awards(1, 1)
        self.assert_points_and_awards(0, 0, 24)
        self.assert_points_and_awards(0, 0, 0)
