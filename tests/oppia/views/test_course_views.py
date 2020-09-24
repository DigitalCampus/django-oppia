
from django.core.paginator import InvalidPage
from django.urls import reverse
from oppia.test import OppiaTestCase


class CourseViewsTest(OppiaTestCase):

    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']

    course_list_template = 'course/list.html'
    course_export_template = 'course/export.html'

    STR_URL_TAG_COURSES = 'oppia:tag_courses'
    STR_URL_COURSE_EXPORTS = 'oppia:course_data_exports'

    def test_tag_view(self):
        self.client.force_login(user=self.admin_user)
        url = reverse(self.STR_URL_TAG_COURSES, args=[2])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.course_list_template)

    def test_tag_view_draft(self):
        self.client.force_login(user=self.admin_user)
        url = reverse(self.STR_URL_TAG_COURSES, args=[2])
        response = self.client.get('%s?visibility=draft' % url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.course_list_template)

    def test_tag_view_archived(self):
        self.client.force_login(user=self.admin_user)
        url = reverse(self.STR_URL_TAG_COURSES, args=[2])
        response = self.client.get('%s?visibility=archived' % url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.course_list_template)

    def test_tag_view_get_page_1(self):
        self.client.force_login(user=self.admin_user)
        url = '%s?page=1' % reverse(self.STR_URL_TAG_COURSES, args=[2])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.course_list_template)

    def test_tag_view_get_page_9999(self):
        self.client.force_login(user=self.admin_user)
        url = '%s?page=9999' % reverse(self.STR_URL_TAG_COURSES, args=[2])
        response = self.client.get(url)
        self.assertRaises(InvalidPage)
        self.assertEqual(404, response.status_code)
        self.assertTemplateUsed(self.course_list_template)

    def test_tag_view_get_page_abc(self):
        self.client.force_login(user=self.admin_user)
        url = '%s?page=abc' % reverse(self.STR_URL_TAG_COURSES, args=[2])
        response = self.client.get(url)
        self.assertRaises(ValueError)
        self.assertEqual(404, response.status_code)
        self.assertTemplateUsed(self.course_list_template)

    def test_export_permissions_admin(self):
        self.client.force_login(user=self.admin_user)
        url = reverse(self.STR_URL_COURSE_EXPORTS, args=[1])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.course_export_template)

    def test_export_permissions_staff(self):
        self.client.force_login(user=self.staff_user)
        url = reverse(self.STR_URL_COURSE_EXPORTS, args=[1])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.course_export_template)

    def test_export_permissions_teacher(self):
        self.client.force_login(user=self.teacher_user)
        url = reverse(self.STR_URL_COURSE_EXPORTS, args=[1])
        response = self.client.get(url)
        self.assertEqual(403, response.status_code)
        self.assertTemplateUsed('403.html')

    def test_export_permissions_normal(self):
        self.client.force_login(user=self.normal_user)
        url = reverse(self.STR_URL_COURSE_EXPORTS, args=[1])
        response = self.client.get(url)
        self.assertEqual(403, response.status_code)
        self.assertTemplateUsed('403.html')

    def test_export_invalid_course(self):
        self.client.force_login(user=self.admin_user)
        url = reverse(self.STR_URL_COURSE_EXPORTS, args=[0])
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)
        self.assertTemplateUsed('404.html')
