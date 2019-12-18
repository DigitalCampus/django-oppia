from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from oppia.models import Course

class MainModelsTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']

    # test course.__unicode__()
    def test_course_get_title(self):
        course = Course.objects.get(pk=1)
        self.assertEqual(course.get_title(), 'Antenatal Care Part 1')
        

# @TODO test course.is_first_download()

# @TODO test course.no_downloads()

# @TODO test course.no_distinct_downloads()