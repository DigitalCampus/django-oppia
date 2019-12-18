from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from oppia.models import Course, Activity

class MainModelsTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']

    def setUp(self):
        self.course = Course.objects.get(pk=1)

    # test course.__unicode__()
    def test_course_get_title(self):
        self.assertEqual(self.course.get_title(), 'Antenatal Care Part 1')
        

    # @TODO test course.is_first_download()
    # def test_course_first_download(self):

    # @TODO test course.no_downloads()

    # test course.no_distinct_downloads()
    def test_course_no_distinct_downloads(self):
        self.assertEqual(self.course.no_distinct_downloads(), 0)

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
    # @TODO Activity has previous
        