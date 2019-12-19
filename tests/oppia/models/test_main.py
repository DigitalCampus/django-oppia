from django.test import TestCase
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCaseMixin

from oppia.models import Course, Activity, Tracker

from tests.user_logins import ADMIN_USER, \
                              STAFF_USER, \
                              NORMAL_USER, \
                              TEACHER_USER

MAIN_FIXTURES = ['tests/test_user.json',
                 'tests/test_oppia.json',
                 'tests/test_quiz.json',
                 'tests/test_permissions.json',
                 'default_gamification_events.json',
                 'tests/test_tracker.json']

class MainModelsCoreTest(ResourceTestCaseMixin, TestCase):
    fixtures = MAIN_FIXTURES

    def setUp(self):
        self.course = Course.objects.get(pk=1)
        self.admin_user = User.objects.get(pk=ADMIN_USER['id'])
        self.staff_user = User.objects.get(pk=STAFF_USER['id'])
        self.teacher_user = User.objects.get(pk=TEACHER_USER['id'])
        self.normal_user = User.objects.get(pk=NORMAL_USER['id'])

        # test course.__unicode__()
    def test_course_get_title(self):
        self.assertEqual(self.course.get_title(), 'Antenatal Care Part 1')

     # test course.no_distinct_downloads()
    def test_course_no_distinct_downloads(self):
        self.assertEqual(self.course.no_distinct_downloads(), 4)

    def test_course_get_activity_today(self):
        self.assertEqual(self.course.get_activity_today(), 0)

    def test_course_get_activity_week(self):
        self.assertEqual(self.course.get_activity_week(), 0)
        
    def test_course_has_quizzes(self):
        self.assertEqual(self.course.has_quizzes(), True)

    def test_course_has_feedback(self):
        self.assertEqual(self.course.has_feedback(), False)
        
    # Activity has next
    def test_activity_next_activity_within_section(self):
        activity = Activity.objects.get(pk=3)
        self.assertEqual(activity.get_next_activity().digest,
                         'fe67f01e97820f2b5b003bf9bfd9f45a12139')

    def test_activity_next_activity_outside_section(self):
        activity = Activity.objects.get(pk=18)
        self.assertEqual(activity.get_next_activity().digest,
                         'f9f0e86f5c5f18a719da21d62a3a9b0c12154')

    def test_activity_next_activity_end_of_course(self):
        activity = Activity.objects.get(pk=222)
        self.assertEqual(activity.get_next_activity(), None)
        
    # Activity has previous
    def test_activity_previous_activity_within_section(self):
        activity = Activity.objects.get(pk=3)
        self.assertEqual(activity.get_previous_activity().digest,
                         '11cc12291f730160c324b727dd2268b612137')

    def test_activity_previous_activity_outside_section(self):
        activity = Activity.objects.get(pk=19)
        self.assertEqual(activity.get_previous_activity().digest,
                         'd95762029b6285dae57385341145c40112153cr0s2a1p80a0')

    def test_activity_previous_activity_beginning_of_course(self):
        activity = Activity.objects.get(pk=1)
        self.assertEqual(activity.get_previous_activity(), None)
    
class MainModelsCourseDownloadloadsNoneTest(ResourceTestCaseMixin, TestCase):
    fixtures = MAIN_FIXTURES

    def setUp(self):
        self.course = Course.objects.get(pk=1)
        self.admin_user = User.objects.get(pk=ADMIN_USER['id'])
        self.staff_user = User.objects.get(pk=STAFF_USER['id'])
        self.teacher_user = User.objects.get(pk=TEACHER_USER['id'])
        self.normal_user = User.objects.get(pk=NORMAL_USER['id'])
        
    # test course is_first_download()
    def test_course_first_download_admin(self):
        Tracker.objects.filter(user=self.admin_user,
                               course=self.course,
                               type='download').delete()
        self.assertTrue(self.course.is_first_download(self.admin_user))

    def test_course_first_download_staff(self):
        Tracker.objects.filter(user=self.staff_user,
                               course=self.course,
                               type='download').delete()
        self.assertTrue(self.course.is_first_download(self.staff_user))

    def test_course_first_download_teacher(self):
        Tracker.objects.filter(user=self.teacher_user,
                               course=self.course,
                               type='download').delete()
        self.assertTrue(self.course.is_first_download(self.teacher_user))

    def test_course_first_download_user(self):
        Tracker.objects.filter(user=self.normal_user,
                               course=self.course,
                               type='download').delete()
        self.assertTrue(self.course.is_first_download(self.normal_user))

class MainModelsCourseDownloadloadsTest(ResourceTestCaseMixin, TestCase):
    fixtures = MAIN_FIXTURES

    def setUp(self):
        self.course = Course.objects.get(pk=1)
        self.admin_user = User.objects.get(pk=ADMIN_USER['id'])
        self.staff_user = User.objects.get(pk=STAFF_USER['id'])
        self.teacher_user = User.objects.get(pk=TEACHER_USER['id'])
        self.normal_user = User.objects.get(pk=NORMAL_USER['id'])

    # test course is not first_download()
    def test_course_not_first_download_admin(self):
        self.assertFalse(self.course.is_first_download(self.admin_user))

    def test_course_not_first_download_staff(self):
        self.assertFalse(self.course.is_first_download(self.staff_user))

    def test_course_not_first_download_teacher(self):
        self.assertFalse(self.course.is_first_download(self.teacher_user))

    def test_course_not_first_download_user(self):
        self.assertFalse(self.course.is_first_download(self.normal_user))
   
        