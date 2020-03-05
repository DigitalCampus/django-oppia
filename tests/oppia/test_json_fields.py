from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from oppia.models import Course, Section, Activity


class JsonFieldsTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json']

    STR_NEW_COURSE_TITLE = "My new course"
    STR_NEW_SECTION_TITLE = "My new section"
    STR_ACTIVITY_TITLE = "My activity"

    # helpers
    def create_course(self, title):
        new_course = Course(title=title, version=1)
        new_course.save()
        return new_course

    def create_section(self, title):
        new_course = self.create_course('{"en": "My new course"}')
        new_section = Section(title=title, course=new_course, order=1)
        new_section.save()
        return new_section

    def create_activity(self, title, content=''):
        new_section = self.create_section('{"en": "My section"}')
        new_activity = Activity(title=title,
                                content=content,
                                section=new_section,
                                order=1)
        new_activity.save()
        return new_activity

    # tests
    def test_course_title_json(self):
        new_course = self.create_course('{"en": "My new course"}')
        self.assertEqual(new_course.get_title(), self.STR_NEW_COURSE_TITLE)

    def test_course_title_plain_text(self):
        new_course = self.create_course('My new course')
        self.assertEqual(new_course.get_title(), self.STR_NEW_COURSE_TITLE)

    def test_course_title_json_multilang(self):
        new_course = self.create_course('{"en": "My new course", \
                                         "es": "Mi nuevo curso"}')
        self.assertEqual(new_course.get_title("es"), 'Mi nuevo curso')

        # test lang that's not defined
        self.assertEqual(new_course.get_title("fi"), self.STR_NEW_COURSE_TITLE)

    def test_course_title_invalid_json(self):
        new_course = self.create_course('{"en": "My new course}')
        self.assertEqual(new_course.get_title(), '{"en": "My new course}')

    def test_section_title_json(self):
        new_section = self.create_section(
            '{"en": \"' + self.STR_NEW_SECTION_TITLE + '\"}')
        self.assertEqual(new_section.get_title(), self.STR_NEW_SECTION_TITLE)

    def test_section_title_plain_text(self):
        new_section = self.create_section(self.STR_NEW_SECTION_TITLE)
        self.assertEqual(new_section.get_title(), self.STR_NEW_SECTION_TITLE)

    def test_section_title_json_multilang(self):
        new_section = self.create_section('{"en": "My new section", \
                                           "es": "Mi nuevo session"}')
        self.assertEqual(new_section.get_title("es"), 'Mi nuevo session')

        # test lang that's not defined
        self.assertEqual(new_section.get_title("fi"),
                         self.STR_NEW_SECTION_TITLE)

    def test_section_title_invalid_json(self):
        new_section = self.create_section('{"en" My new section"}')
        self.assertEqual(new_section.get_title(), '{"en" My new section"}')

    def test_activity_title_json(self):
        new_activity = self.create_activity('{"en": "My activity"}')
        self.assertEqual(new_activity.get_title(), self.STR_ACTIVITY_TITLE)

    def test_activity_title_plain_text(self):
        new_activity = self.create_activity('My activity')
        self.assertEqual(new_activity.get_title(), self.STR_ACTIVITY_TITLE)

    def test_activity_title_json_multilang(self):
        new_activity = self.create_activity('{"en": "My activity", \
                                             "es": "Mi actividad"}')
        self.assertEqual(new_activity.get_title("es"), 'Mi actividad')

        # test lang that's not defined
        self.assertEqual(new_activity.get_title("fi"), 'My activity')

    def test_activity_title_invalid_json(self):
        new_activity = self.create_activity('{"en" My activity"}')
        self.assertEqual(new_activity.get_title(), '{"en" My activity"}')

    def test_activity_content_json(self):
        new_activity = self.create_activity('{"en": "My activity"}',
                                            '{"en": "09_427_en.html"}')
        self.assertEqual(new_activity.get_content(), '09_427_en.html')

    def test_activity_content_plain_text(self):
        new_activity = self.create_activity('{"en": "My activity"}',
                                            '09_427_en.html')
        self.assertEqual(new_activity.get_content(), '09_427_en.html')

    def test_activity_content_multilang(self):
        new_activity = self.create_activity('{"en": "My activity"}',
                                            '{"en": "09_427_en.html", \
                                             "es": "09_427_es.html"}')
        self.assertEqual(new_activity.get_content("es"), '09_427_es.html')
        # test lang that's not defined
        self.assertEqual(new_activity.get_content("fi"), '09_427_en.html')

    def test_activity_content_invalid_json(self):
        new_activity = self.create_activity('{"en": "My activity"}',
                                            '{"en": "09_427_en.html')
        self.assertEqual(new_activity.get_content(), '{"en": "09_427_en.html')
