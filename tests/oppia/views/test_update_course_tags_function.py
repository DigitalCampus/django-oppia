from django.contrib.auth.models import User
from django.test import TestCase

from tests.user_logins import ADMIN_USER
from oppia.forms.upload import UploadCourseStep2Form
from oppia.models import Course, CourseTag, Tag
from oppia.views import update_course_tags

class UpdateCourseTagsFunctionTest(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json']

    def setUp(self):
        super(UpdateCourseTagsFunctionTest, self).setUp()

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
        user = User.objects.get(username=ADMIN_USER['user'])
        new_tags = course.get_tags() + ', my new tag'

        coursetag_count_start = CourseTag.objects.filter(course=course).count()
        tag_count_start = Tag.objects.all().count()

        request_post = {'tags': new_tags,
                        'is_draft': course.is_draft, }
        form = UploadCourseStep2Form(request_post)
        self.assertEqual(form.is_valid(), True)

        update_course_tags(form, course, user)

        coursetag_count_end = CourseTag.objects.filter(course=course).count()
        self.assertEqual(coursetag_count_start+1, coursetag_count_end)

        tag_count_end = Tag.objects.all().count()
        self.assertEqual(tag_count_start+1, tag_count_end)

    def test_add_tags(self):
        course = Course.objects.get(pk=1)
        user = User.objects.get(username=ADMIN_USER['user'])
        new_tags = course.get_tags() + ', my new tag, another new tag'

        coursetag_count_start = CourseTag.objects.filter(course=course).count()
        tag_count_start = Tag.objects.all().count()

        request_post = {'tags': new_tags,
                        'is_draft': course.is_draft, }
        form = UploadCourseStep2Form(request_post)
        self.assertEqual(form.is_valid(), True)

        update_course_tags(form, course, user)

        coursetag_count_end = CourseTag.objects.filter(course=course).count()
        self.assertEqual(coursetag_count_start+2, coursetag_count_end)

        tag_count_end = Tag.objects.all().count()
        self.assertEqual(tag_count_start+2, tag_count_end)

    def test_remove_one_tag(self):
        course = Course.objects.get(pk=1)
        user = User.objects.get(username=ADMIN_USER['user'])
        new_tags = 'HEAT, ANC'

        coursetag_count_start = CourseTag.objects.filter(course=course).count()
        tag_count_start = Tag.objects.all().count()

        request_post = {'tags': new_tags,
                        'is_draft': course.is_draft, }
        form = UploadCourseStep2Form(request_post)
        self.assertEqual(form.is_valid(), True)

        update_course_tags(form, course, user)

        coursetag_count_end = CourseTag.objects.filter(course=course).count()
        self.assertEqual(coursetag_count_start-1, coursetag_count_end)

        tag_count_end = Tag.objects.all().count()
        self.assertEqual(tag_count_start, tag_count_end)

    def test_remove_tags(self):
        course = Course.objects.get(pk=1)
        user = User.objects.get(username=ADMIN_USER['user'])
        new_tags = 'HEAT'

        coursetag_count_start = CourseTag.objects.filter(course=course).count()
        tag_count_start = Tag.objects.all().count()

        request_post = {'tags': new_tags,
                        'is_draft': course.is_draft, }
        form = UploadCourseStep2Form(request_post)
        self.assertEqual(form.is_valid(), True)

        update_course_tags(form, course, user)

        coursetag_count_end = CourseTag.objects.filter(course=course).count()
        self.assertEqual(coursetag_count_start-2, coursetag_count_end)

        tag_count_end = Tag.objects.all().count()
        self.assertEqual(tag_count_start, tag_count_end)
