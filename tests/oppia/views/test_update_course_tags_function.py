from oppia.test import OppiaTestCase

from oppia.forms.upload import UploadCourseStep2Form
from oppia.models import Course, CourseTag, Tag
from oppia.views import CourseFormView


class UpdateCourseTagsFunctionTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']

    def test_no_tags(self):
        course = Course.objects.get(pk=1)
        coursetag_count_start = CourseTag.objects.filter(course=course).count()
        request_post = {'tags': '',
                        'is_draft': course.is_draft, }
        form = UploadCourseStep2Form(request_post)
        self.assertEqual(form.is_valid(), False)
        coursetag_count_end = CourseTag.objects.filter(course=course).count()
        self.assertEqual(coursetag_count_start, coursetag_count_end)

    def test_empty_tag(self):
        course = Course.objects.get(pk=1)
        coursetag_count_start = CourseTag.objects.filter(course=course).count()
        request_post = {'tags': '    ',
                        'is_draft': course.is_draft, }
        form = UploadCourseStep2Form(request_post)
        self.assertEqual(form.is_valid(), False)
        coursetag_count_end = CourseTag.objects.filter(course=course).count()
        self.assertEqual(coursetag_count_start, coursetag_count_end)

    def test_add_one_tag(self):
        course = Course.objects.get(pk=1)
        new_tags = course.get_tags() + ', my new tag'

        coursetag_count_start = CourseTag.objects.filter(course=course).count()
        tag_count_start = Tag.objects.all().count()

        request_post = {'tags': new_tags,
                        'is_draft': course.is_draft, }
        form = UploadCourseStep2Form(request_post)
        self.assertEqual(form.is_valid(), True)

        cfv = CourseFormView()
        cfv.update_course_tags(form, course, self.admin_user)

        coursetag_count_end = CourseTag.objects.filter(course=course).count()
        self.assertEqual(coursetag_count_start+1, coursetag_count_end)

        tag_count_end = Tag.objects.all().count()
        self.assertEqual(tag_count_start+1, tag_count_end)

    def test_add_tags(self):
        course = Course.objects.get(pk=1)
        new_tags = course.get_tags() + ', my new tag, another new tag'

        coursetag_count_start = CourseTag.objects.filter(course=course).count()
        tag_count_start = Tag.objects.all().count()

        request_post = {'tags': new_tags,
                        'is_draft': course.is_draft, }
        form = UploadCourseStep2Form(request_post)
        self.assertEqual(form.is_valid(), True)

        cfv = CourseFormView()
        cfv.update_course_tags(form, course, self.admin_user)

        coursetag_count_end = CourseTag.objects.filter(course=course).count()
        self.assertEqual(coursetag_count_start+2, coursetag_count_end)

        tag_count_end = Tag.objects.all().count()
        self.assertEqual(tag_count_start+2, tag_count_end)

    def test_remove_one_tag(self):
        course = Course.objects.get(pk=1)
        new_tags = 'HEAT, ANC'

        coursetag_count_start = CourseTag.objects.filter(course=course).count()
        tag_count_start = Tag.objects.all().count()

        request_post = {'tags': new_tags,
                        'is_draft': course.is_draft, }
        form = UploadCourseStep2Form(request_post)
        self.assertEqual(form.is_valid(), True)

        cfv = CourseFormView()
        cfv.update_course_tags(form, course, self.admin_user)

        coursetag_count_end = CourseTag.objects.filter(course=course).count()
        self.assertEqual(coursetag_count_start-1, coursetag_count_end)

        tag_count_end = Tag.objects.all().count()
        self.assertEqual(tag_count_start, tag_count_end)

    def test_remove_tags(self):
        course = Course.objects.get(pk=1)
        new_tags = 'HEAT'

        coursetag_count_start = CourseTag.objects.filter(course=course).count()
        tag_count_start = Tag.objects.all().count()

        request_post = {'tags': new_tags,
                        'is_draft': course.is_draft, }
        form = UploadCourseStep2Form(request_post)
        self.assertEqual(form.is_valid(), True)

        cfv = CourseFormView()
        cfv.update_course_tags(form, course, self.admin_user)

        coursetag_count_end = CourseTag.objects.filter(course=course).count()
        self.assertEqual(coursetag_count_start-2, coursetag_count_end)

        tag_count_end = Tag.objects.all().count()
        self.assertEqual(tag_count_start, tag_count_end)
