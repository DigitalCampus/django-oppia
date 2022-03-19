from django.core.management import call_command

from io import StringIO

from django.contrib.auth.models import User

from oppia.test import OppiaTestCase
from oppia.models import Course
from summary.models import UserCourseSummary


'''
Test Data:

3 versions of course
v1 - page 1v1, page 2v1, page 3v1, quiz 1v1, feedback 1v1
v2 - page 1v2, page 2v1, page 3v1, quiz 1v2, feedback 1v1, page 4v1
v3 - page 1v2, page 2v1, page 3v1, quiz 1v3, feedback 1v2


3 Users
User A
course-v1 - page 1v1,
            page 2v1 completed,
            quiz 1v1 attempted twice,
            feedback 1v1 completed
    expected:
        total_activity - 5,
        completed_activities - 3,
        total_activity_current - 5,
        total_activity_previous - 0
course-v2 - page 1v2,
            page 2v1 completed,
            quiz 1v2 passed,
            page 4v1 completed
    expected:
        total_activity - 9,
        completed_activities - 5,
        total_activity_current - 6,
        total_activity_previous - 3
course-v3 - page 3v1 completed,
            feedback 1v2 completed
    expected:
        total_activity - 11,
        completed_activities - 4,
        total_activity_current - 5
        total_activity_previous - 6

User B
course-v1 - no activity
    expected:
        total_activity - 0,
        completed_activities - 0,
        total_activity_current - 0,
        total_activity_previous - 0
course-v2 - p1v2 completed twice,
            quiz1v2 complete (passed)
    expected:
        total_activity - 3,
        completed_activities - 2,
        total_activity_current - 3,
        total_activity_previous - 0
course-v3 - page2v1 complete,
            feedback 1v2 complete,
            quiz 1v3 passed
    expected:
        total_activity - 6,
        completed_activities - 4,
        total_activity_current - 5,
        total_activity_previous - 1

User C
course-v1 - no activity
    expected:
        total_activity - 0,
        completed_activities - 0,
        total_activity_current - 0,
        total_activity_previous - 0
course-v2 - no activity
    expected:
        total_activity - 0,
        completed_activities - 0,
        total_activity_current - 0,
        total_activity_previous - 0
course-v3 - page 1v2 twice,
            page 2v1,
            quiz 1v3 passed
    expected:
        total_activity - 4,
        completed_activities - 3,
        total_activity_current - 4,
        total_activity_previous - 0

'''

COURSE_SHORTNAME = "oppia800course"

JSON_GAMIFICATION = 'default_gamification_events.json'
JSON_BADGES = 'default_badges.json'
JSON_USERS = 'tests/usercoursesummary/user.json'


class UserCourseSummaryTestCourseV1(OppiaTestCase):

    fixtures = [JSON_GAMIFICATION,
                JSON_BADGES,
                JSON_USERS,
                'tests/usercoursesummary/course_tracker_v1.json']

    def setUp(self):
        self.course = Course.objects.get(shortname=COURSE_SHORTNAME)
        self.user_a = User.objects.get(username="user_a")
        self.user_b = User.objects.get(username="user_b")
        self.user_c = User.objects.get(username="user_c")

    def test_incremental(self):
        call_command('update_summaries', stdout=StringIO())
        self.check_summary_values()

    def test_fromstart(self):
        call_command('update_summaries', '--fromstart', stdout=StringIO())
        self.check_summary_values()

    def check_summary_values(self):
        # User A
        user_a_summary = UserCourseSummary.objects.get(
            course=self.course,
            user=self.user_a)
        self.assertEqual(5, user_a_summary.total_activity)
        self.assertEqual(3, user_a_summary.completed_activities)
        self.assertEqual(5, user_a_summary.total_activity_current)
        self.assertEqual(0, user_a_summary.total_activity_previous)
        self.assertEqual(1, user_a_summary.total_downloads)
        self.assertEqual(0, user_a_summary.quizzes_passed)

        # User B
        with self.assertRaises(UserCourseSummary.DoesNotExist):
            UserCourseSummary.objects.get(course=self.course, user=self.user_b)

        # User C
        with self.assertRaises(UserCourseSummary.DoesNotExist):
            UserCourseSummary.objects.get(course=self.course, user=self.user_c)


class UserCourseSummaryTestCourseV2(OppiaTestCase):

    fixtures = [JSON_GAMIFICATION,
                JSON_BADGES,
                JSON_USERS,
                'tests/usercoursesummary/course_tracker_v2.json',
                'tests/usercoursesummary/settings_summary_v1.json']

    def setUp(self):
        self.course = Course.objects.get(shortname=COURSE_SHORTNAME)
        self.user_a = User.objects.get(username="user_a")
        self.user_b = User.objects.get(username="user_b")
        self.user_c = User.objects.get(username="user_c")

    def test_incremental(self):
        call_command('update_summaries', stdout=StringIO())
        self.check_summary_values()

    def test_fromstart(self):
        call_command('update_summaries', '--fromstart', stdout=StringIO())
        self.check_summary_values()

    def check_summary_values(self):
        # User A
        user_a_summary = UserCourseSummary.objects.get(
            course=self.course,
            user=self.user_a)
        self.assertEqual(9, user_a_summary.total_activity)
        self.assertEqual(5, user_a_summary.completed_activities)
        self.assertEqual(6, user_a_summary.total_activity_current)
        self.assertEqual(3, user_a_summary.total_activity_previous)
        self.assertEqual(2, user_a_summary.total_downloads)
        self.assertEqual(1, user_a_summary.quizzes_passed)

        # User B
        user_b_summary = UserCourseSummary.objects.get(
            course=self.course,
            user=self.user_b)
        self.assertEqual(3, user_b_summary.total_activity)
        self.assertEqual(2, user_b_summary.completed_activities)
        self.assertEqual(3, user_b_summary.total_activity_current)
        self.assertEqual(0, user_b_summary.total_activity_previous)
        self.assertEqual(0, user_b_summary.total_downloads)
        self.assertEqual(1, user_b_summary.quizzes_passed)

        # User C
        with self.assertRaises(UserCourseSummary.DoesNotExist):
            UserCourseSummary.objects.get(course=self.course, user=self.user_c)


class UserCourseSummaryTestCourseV3(OppiaTestCase):

    fixtures = [JSON_GAMIFICATION,
                JSON_BADGES,
                JSON_USERS,
                'tests/usercoursesummary/course_tracker_v3.json',
                'tests/usercoursesummary/settings_summary_v2.json']

    def setUp(self):
        self.course = Course.objects.get(shortname=COURSE_SHORTNAME)
        self.user_a = User.objects.get(username="user_a")
        self.user_b = User.objects.get(username="user_b")
        self.user_c = User.objects.get(username="user_c")

    def test_incremental(self):
        call_command('update_summaries', stdout=StringIO())
        self.check_summary_values()

    def test_fromstart(self):
        call_command('update_summaries', '--fromstart', stdout=StringIO())
        self.check_summary_values()

    def check_summary_values(self):
        # User A
        user_a_summary = UserCourseSummary.objects.get(
            course=self.course,
            user=self.user_a)
        self.assertEqual(11, user_a_summary.total_activity)
        self.assertEqual(4, user_a_summary.completed_activities)
        self.assertEqual(5, user_a_summary.total_activity_current)
        self.assertEqual(6, user_a_summary.total_activity_previous)
        self.assertEqual(3, user_a_summary.total_downloads)
        self.assertEqual(0, user_a_summary.quizzes_passed)

        # User B
        user_b_summary = UserCourseSummary.objects.get(
            course=self.course,
            user=self.user_b)
        self.assertEqual(6, user_b_summary.total_activity)
        self.assertEqual(4, user_b_summary.completed_activities)
        self.assertEqual(5, user_b_summary.total_activity_current)
        self.assertEqual(1, user_b_summary.total_activity_previous)
        self.assertEqual(0, user_b_summary.total_downloads)
        self.assertEqual(1, user_b_summary.quizzes_passed)

        # User C
        user_c_summary = UserCourseSummary.objects.get(
            course=self.course,
            user=self.user_c)
        self.assertEqual(4, user_c_summary.total_activity)
        self.assertEqual(3, user_c_summary.completed_activities)
        self.assertEqual(4, user_c_summary.total_activity_current)
        self.assertEqual(0, user_c_summary.total_activity_previous)
        self.assertEqual(0, user_c_summary.total_downloads)
        self.assertEqual(1, user_c_summary.quizzes_passed)
