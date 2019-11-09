from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from oppia.models import Course, Section


class JsonFieldsTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json']

    def test_course_title_json(self):
        course_title = '{"en": "My new course"}'
        new_course = Course(title=course_title, version=1)
        new_course.save()

        self.assertEqual(new_course.get_title(), 'My new course')

    def test_course_title_plain_text(self):
        course_title = 'My new course'
        new_course = Course(title=course_title, version=1)
        new_course.save()

        self.assertEqual(new_course.get_title(), 'My new course')

    def test_course_title_json_multilang(self):
        course_title = '{"en": "My new course", "es": "Mi nuevo curso"}'
        new_course = Course(title=course_title, version=1)
        new_course.save()

        self.assertEqual(new_course.get_title("es"), 'Mi nuevo curso')

        # test lang that's not defined
        self.assertEqual(new_course.get_title("fi"), 'My new course')

    def test_course_title_invalid_json(self):
        course_title = '{"en": "My new course}'
        new_course = Course(title=course_title, version=1)
        new_course.save()

        self.assertEqual(new_course.get_title(), '{"en": "My new course}')

    def test_section_title_json(self):
        course_title = '{"en": "My new course"}'
        new_course = Course(title=course_title, version=1)
        new_course.save()

        section_title = '{"en": "My new section"}'
        new_section = Section(title=section_title, course=new_course, order=1)
        new_section.save()

        self.assertEqual(new_section.get_title(), 'My new section')

    def test_section_title_plain_text(self):
        course_title = 'My new course'
        new_course = Course(title=course_title, version=1)
        new_course.save()

        section_title = 'My new section'
        new_section = Section(title=section_title, course=new_course, order=1)
        new_section.save()

        self.assertEqual(new_section.get_title(), 'My new section')

    def test_section_title_json_multilang(self):
        course_title = '{"en": "My new course", "es": "Mi nuevo curso"}'
        new_course = Course(title=course_title, version=1)
        new_course.save()

        section_title = '{"en": "My new section", "es": "Mi nuevo session"}'
        new_section = Section(title=section_title, course=new_course, order=1)
        new_section.save()

        self.assertEqual(new_section.get_title("es"), 'Mi nuevo session')

        # test lang that's not defined
        self.assertEqual(new_section.get_title("fi"), 'My new section')

    def test_section_title_invalid_json(self):
        course_title = '{"en": "My new course}'
        new_course = Course(title=course_title, version=1)
        new_course.save()

        section_title = '{"en" My new section"}'
        new_section = Section(title=section_title, course=new_course, order=1)
        new_section.save()

        self.assertEqual(new_section.get_title(), '{"en" My new section"}')
