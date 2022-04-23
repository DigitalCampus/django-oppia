import os
import shutil
from zipfile import ZipFile

import pytest

from django.conf import settings
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_url, update_course_visibility


class CourseStructureResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'default_badges.json']

    TEST_COURSES = ['anc_test_course.zip']

    @classmethod
    def copy_test_courses(cls):
        for test_course in cls.TEST_COURSES:
            if not os.path.isfile(test_course):
                src = os.path.join(settings.TEST_RESOURCES, test_course)
                dst = os.path.join(settings.MEDIA_ROOT, 'courses', test_course)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(src, dst)

    @classmethod
    def extract_test_courses(cls):
        extract_path = os.path.join(settings.MEDIA_ROOT, 'courses')
        for file in os.listdir(extract_path):
            if file.endswith('.zip'):
                with ZipFile(os.path.join(extract_path, file), 'r') as zip_file:
                    zip_file.extractall(path=extract_path)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.copy_test_courses()
        cls.extract_test_courses()

    # working id
    def test_working_id(self):
        url = get_api_url('v2', 'coursestructure', 1)
        response = self.client.get(url)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)

    # working shortname
    def test_working_shortname(self):
        url = get_api_url('v2', 'coursestructure', 'anc1-all')
        response = self.client.get(url)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)

    # non-existent course id
    def test_invalid_id(self):
        url = get_api_url('v2', 'coursestructure', 0)
        response = self.client.get(url)
        self.assertHttpNotFound(response)

    # non-existent course shortname
    def test_invalid_shortname(self):
        url = get_api_url('v2', 'coursestructure', 'not-a-course')
        response = self.client.get(url)
        self.assertHttpNotFound(response)

    # draft course with id
    def test_draft_id(self):
        update_course_visibility(1, True, False)
        url = get_api_url('v2', 'coursestructure', 1)
        response = self.client.get(url)
        self.assertHttpNotFound(response)

    # draft course with shortname
    def test_draft_shortname(self):
        update_course_visibility(1, True, False)
        url = get_api_url('v2', 'coursestructure', 'anc1-all')
        response = self.client.get(url)
        self.assertHttpNotFound(response)

    # archived course with id
    def test_archived_id(self):
        update_course_visibility(1, False, True)
        url = get_api_url('v2', 'coursestructure', 1)
        response = self.client.get(url)
        self.assertHttpNotFound(response)

    # archived course with shortname
    def test_archived_shortname(self):
        update_course_visibility(1, False, True)
        url = get_api_url('v2', 'coursestructure', 'anc1-all')
        response = self.client.get(url)
        self.assertHttpNotFound(response)

    # no module.xml found
    def test_no_module_xml(self):
        url = get_api_url('v2', 'coursestructure', 999)
        response = self.client.get(url)
        self.assertHttpNotFound(response)
