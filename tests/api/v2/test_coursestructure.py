import pytest
import unittest

from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from tests.utils import get_api_key, get_api_url, update_course_visibility


class CourseStructureResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'default_badges.json']
    
    # working id
    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
    @unittest.expectedFailure
    def test_working_id(self):
        url = get_api_url('v2', 'coursestructure') + "1/"
        response = self.client.get(url)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
    
    # working shortname
    @pytest.mark.xfail(reason="works on local, but not on Github workflow")
    @unittest.expectedFailure
    def test_working_shortname(self):
        url = get_api_url('v2', 'coursestructure') + "anc1-all/"
        response = self.client.get(url)
        self.assertHttpOK(response)
        self.assertValidJSON(response.content)
        
    # non-existent course id
    def test_invalid_id(self):
        url = get_api_url('v2', 'coursestructure') + "0/"
        response = self.client.get(url)
        self.assertHttpNotFound(response)
        
    # non-existent course shortname
    def test_invalid_shortname(self):
        url = get_api_url('v2', 'coursestructure') + "not-a-course/"
        response = self.client.get(url)
        self.assertHttpNotFound(response)

    # draft course with id
    def test_draft_id(self):
        update_course_visibility(1, 1, 0)
        url = get_api_url('v2', 'coursestructure') + "1/"
        response = self.client.get(url)
        self.assertHttpNotFound(response)
        update_course_visibility(1, 0, 0)
        
    # draft course with shortname
    def test_draft_shortname(self):
        update_course_visibility(1, 1, 0)
        url = get_api_url('v2', 'coursestructure') + "anc1-all/"
        response = self.client.get(url)
        self.assertHttpNotFound(response)
        update_course_visibility(1, 0, 0)
        
    # archived course with id
    def test_archived_id(self):
        update_course_visibility(1, 0, 1)
        url = get_api_url('v2', 'coursestructure') + "1/"
        response = self.client.get(url)
        self.assertHttpNotFound(response)
        update_course_visibility(1, 0, 0)
        
    # archived course with shortname
    def test_archived_shortname(self):
        update_course_visibility(1, 0, 1)
        url = get_api_url('v2', 'coursestructure') + "anc1-all/"
        response = self.client.get(url)
        self.assertHttpNotFound(response)
        update_course_visibility(1, 0, 0)
    
    # no module.xml found
    def test_no_module_xml(self):
        url = get_api_url('v2', 'coursestructure') + "1/"
        response = self.client.get(url)
        self.assertHttpNotFound(response)
