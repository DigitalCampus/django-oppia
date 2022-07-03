from django.contrib.admin import AdminSite
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpRequest

from oppia.admin import CourseStatusAdmin
from oppia.models import CourseStatus, Course
from oppia.test import OppiaTestCase
from tests.utils import update_course_status


class CourseStatusModelTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_course_statuses.json',
                'tests/test_oppia.json',
                'tests/test_course_permissions.json']

    def setUp(self):
        super().setUp()
        self.request = HttpRequest()
        setattr(self.request, 'session', 'session')
        messages = FallbackStorage(self.request)
        setattr(self.request, '_messages', messages)

    def test_deactivate_unused_status(self):
        courses = Course.objects.all()
        # 1. Set all courses to 'Live' status
        for course in courses:
            update_course_status(course.id, CourseStatus.LIVE)

        # 2. Force initial availability to True for 'Draft' status
        test_status_name = 'draft'
        draft_status = CourseStatus.objects.get(name=test_status_name)
        draft_status.available = True
        draft_status.save()

        # 3. Simulate updating availability from Admin panel
        draft_status.available = False
        course_status_admin = CourseStatusAdmin(model=CourseStatus, admin_site=AdminSite())
        course_status_admin.save_model(obj=draft_status, request=self.request, form=None, change=None)
        messages = list(get_messages(self.request))

        # 4. Verify successful message and that 'Draft' status is available
        expected_msg = CourseStatusAdmin.SUCCESS_MSG.format(status_name=test_status_name)
        self.assertEqual(expected_msg, str(messages[0]))
        self.assertFalse(CourseStatus.objects.get(name='draft').available)

    def test_activate_unused_status(self):
        courses = Course.objects.all()
        # 1. Set all courses to 'Live' status
        for course in courses:
            update_course_status(course.id, CourseStatus.LIVE)

        # 2. Force initial availability to True for 'Draft' status
        test_status_name = 'draft'
        draft_status = CourseStatus.objects.get(name=test_status_name)
        draft_status.available = False
        draft_status.save()

        # 3. Simulate updating availability from Admin panel
        draft_status.available = True
        course_status_admin = CourseStatusAdmin(model=CourseStatus, admin_site=AdminSite())
        course_status_admin.save_model(obj=draft_status, request=self.request, form=None, change=None)
        messages = list(get_messages(self.request))

        # 4. Verify successful message and that 'Draft' status is available
        expected_msg = CourseStatusAdmin.SUCCESS_MSG.format(status_name=test_status_name)
        self.assertEqual(expected_msg, str(messages[0]))
        self.assertTrue(CourseStatus.objects.get(name='draft').available)

    def test_deactivate_used_status(self):
        test_status_name = 'draft'
        course_id = 1
        # 1. Set course=1 status as Draft
        update_course_status(course_id, CourseStatus.DRAFT)

        # 2. Force initial availability to True for 'Draft' status
        draft_status = CourseStatus.objects.get(name=test_status_name)
        draft_status.available = True
        draft_status.save()

        # 3. Simulate updating availability from Admin panel
        draft_status.available = False
        course_status_admin = CourseStatusAdmin(model=CourseStatus, admin_site=AdminSite())
        course_status_admin.save_model(obj=draft_status, request=self.request, form=None, change=None)
        messages = list(get_messages(self.request))

        # 4. Verify error message and that 'Draft' status is still available
        expected_msg = CourseStatusAdmin.ERROR_MSG.format(status_name=test_status_name)
        self.assertEqual(expected_msg, str(messages[0]))
        self.assertTrue(CourseStatus.objects.get(name='draft').available)

    def test_activate_used_status(self):
        test_status_name = 'draft'
        course_id = 1
        # 1. Set course=1 status as Draft
        update_course_status(course_id, CourseStatus.DRAFT)

        # 2. Force initial availability to False for 'Draft' status
        draft_status = CourseStatus.objects.get(name=test_status_name)
        draft_status.available = False
        draft_status.save()

        # 3. Simulate updating availability from Admin panel
        draft_status.available = True
        course_status_admin = CourseStatusAdmin(model=CourseStatus, admin_site=AdminSite())
        course_status_admin.save_model(obj=draft_status, request=self.request, form=None, change=None)
        messages = list(get_messages(self.request))

        # 4. Verify successful message and that 'Draft' status is available
        expected_msg = CourseStatusAdmin.SUCCESS_MSG.format(status_name=test_status_name)
        self.assertEqual(expected_msg, str(messages[0]))
        self.assertTrue(CourseStatus.objects.get(name='draft').available)

    def test_get_active_statuses(self):
        available_statuses = CourseStatus.objects.available_statuses()
        self.assertTrue(CourseStatus.objects.get(name=CourseStatus.ARCHIVED) in available_statuses)

        archived_status = CourseStatus.objects.get(name='archived')
        archived_status.available = False
        archived_status.save()

        available_statuses = CourseStatus.objects.available_statuses()
        self.assertFalse(CourseStatus.objects.get(name=CourseStatus.ARCHIVED) in available_statuses)
