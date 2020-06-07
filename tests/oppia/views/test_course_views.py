
from django.core.paginator import InvalidPage
from django.urls import reverse
from oppia.test import OppiaTestCase


class CourseViewsTest(OppiaTestCase):

    course_list_template = 'course/list.html'

    def test_tag_view(self):
        self.client.force_login(user=self.admin_user)
        url = reverse('oppia:tag_courses', args=[2])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.course_list_template)

    def test_tag_view_draft(self):
        self.client.force_login(user=self.admin_user)
        url = reverse('oppia:tag_courses', args=[2])
        response = self.client.get('%s?visibility=draft' % url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.course_list_template)

    def test_tag_view_archived(self):
        self.client.force_login(user=self.admin_user)
        url = reverse('oppia:tag_courses', args=[2])
        response = self.client.get('%s?visibility=archived' % url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.course_list_template)

    def test_tag_view_get_page_1(self):
        self.client.force_login(user=self.admin_user)
        url = '%s?page=1' % reverse('oppia:tag_courses', args=[2])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(self.course_list_template)

    def test_tag_view_get_page_9999(self):
        self.client.force_login(user=self.admin_user)
        url = '%s?page=9999' % reverse('oppia:tag_courses', args=[2])
        response = self.client.get(url)
        self.assertRaises(InvalidPage)
        self.assertEqual(404, response.status_code)
        self.assertTemplateUsed(self.course_list_template)

    def test_tag_view_get_page_abc(self):
        self.client.force_login(user=self.admin_user)
        url = '%s?page=abc' % reverse('oppia:tag_courses', args=[2])
        response = self.client.get(url)
        self.assertRaises(ValueError)
        self.assertEqual(404, response.status_code)
        self.assertTemplateUsed(self.course_list_template)
