
from django.urls import reverse
from oppia.test import OppiaTestCase
from oppia.permissions import is_manager_only


class PermissionsViewTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']

    STR_ADMIN_INDEX = 'admin:index'

    def assert_response(self, view, status_code, user=None, view_kwargs=None):
        route = reverse(view, kwargs=view_kwargs)
        res = self.get_view(route, user)
        self.assertEqual(res.status_code, status_code)
        return res

    def assert_must_login(self, view, user=None, view_kwargs=None):
        route = reverse(view, kwargs=view_kwargs)
        res = self.get_view(route, user)
        login_url = self.login_url + '?next=' + route
        self.assertRedirects(res, login_url)
        return res

    def assert_can_view(self, view, user=None, view_kwargs=None):
        return self.assert_response(view, 200, user, view_kwargs)

    def assert_cannot_view(self, view, user=None, view_kwargs=None):
        return self.assert_response(view, 401, user, view_kwargs)

    def assert_unauthorized(self, view, user=None, view_kwargs=None):
        return self.assert_response(view, 403, user, view_kwargs)

    def assert_not_found(self, view, user=None, view_kwargs=None):
        return self.assert_response(view, 404, user, view_kwargs)

    # Django admin

    def test_anon_cantview_admin(self):
        self.assert_must_login(self.STR_ADMIN_INDEX)

    def test_admin_canview_admin(self):
        self.assert_can_view(self.STR_ADMIN_INDEX, self.admin_user)

    def test_staff_cantview_admin(self):
        self.assert_can_view(self.STR_ADMIN_INDEX, self.staff_user)

    def test_student_cantview_admin(self):
        # Check that gets redirected to admin login
        route = reverse(self.STR_ADMIN_INDEX)
        res = self.get_view(route, self.normal_user)
        self.assertRedirects(res, route + 'login/?next=' + route)
    # Upload courses view

    def test_anon_cantview_upload_courses(self):
        self.assert_must_login('oppia:upload')

    def test_admin_canview_upload_courses(self):
        self.assert_can_view('oppia:upload', self.admin_user)

    def test_staff_canview_upload_courses(self):
        self.assert_can_view('oppia:upload', self.staff_user)

    def test_student_cantview_upload_courses(self):
        self.assert_unauthorized('oppia:upload', self.normal_user)

    def test_user_with_canupload_canview_upload_courses(self):
        self.assert_can_view('oppia:upload', self.teacher_user)

    # Bulk upload users view

    def test_anon_cantview_bulk_upload(self):
        self.assert_must_login('profile:upload')

    def test_admin_canview_bulk_upload(self):
        self.assert_can_view('profile:upload', self.admin_user)

    def test_staff_cantview_bulk_upload(self):
        self.assert_unauthorized('profile:upload', self.staff_user)

    def test_student_cantview_bulk_upload(self):
        self.assert_unauthorized('profile:upload', self.normal_user)

    # View cohort list

    def test_anon_cantview_cohorts(self):
        self.assert_must_login('oppia:cohorts')

    def test_admin_canview_cohorts(self):
        self.assert_can_view('oppia:cohorts', self.admin_user)

    def test_staff_canview_cohorts(self):
        self.assert_can_view('oppia:cohorts', self.staff_user)

    def test_student_cantview_cohorts(self):
        self.assert_unauthorized('oppia:cohorts', self.normal_user)
    # TODO: Define a teacher user to test cohort management

    # View a cohort

    def test_anon_cantview_cohort(self):
        self.assert_must_login('oppia:cohort_view',
                               view_kwargs={'pk': 1})

    def test_view_nonexisting_cohort(self):
        self.assert_not_found('oppia:cohort_view',
                              self.admin_user,
                              view_kwargs={'pk': 1000})

    def test_admin_canview_cohort(self):
        self.assert_can_view('oppia:cohort_view',
                             self.admin_user,
                             view_kwargs={'pk': 1})

    def test_staff_canview_cohort(self):
        self.assert_can_view('oppia:cohort_view',
                             self.staff_user,
                             view_kwargs={'pk': 1})

    def test_student_cantview_cohort(self):
        self.assert_unauthorized('oppia:cohort_view',
                                 self.normal_user,
                                 view_kwargs={'pk': 1})
    # TODO: Teacher view cohort s/he is assigned into

    # View a cohort course activity

    def test_anon_cantview_cohort_course(self):
        self.assert_must_login('oppia:cohort_course_view',
                               view_kwargs={'cohort_id': 1, 'course_id': 1})

    def test_view_nonexisting_cohort_course(self):
        self.assert_not_found('oppia:cohort_course_view', self.admin_user,
                              view_kwargs={'cohort_id': 1000,
                                           'course_id': 1000})

    def test_admin_canview_cohort_course(self):
        self.assert_can_view('oppia:cohort_course_view',
                             self.admin_user,
                             view_kwargs={'cohort_id': 1, 'course_id': 1})

    def test_staff_canview_cohort_course(self):
        self.assert_can_view('oppia:cohort_course_view',
                             self.staff_user,
                             view_kwargs={'cohort_id': 1, 'course_id': 1})

    def test_student_cantview_cohort_course(self):
        self.assert_unauthorized('oppia:cohort_course_view', self.normal_user,
                                 view_kwargs={'cohort_id': 1, 'course_id': 1})
    # TODO: Teacher view cohort s/he is assigned into

    # Add new cohort

    def test_anon_cantview_add_cohort(self):
        self.assert_must_login('oppia:cohort_add')

    def test_admin_canview_add_cohort(self):
        self.assert_can_view('oppia:cohort_add', self.admin_user)

    def test_staff_canview_add_cohort(self):
        self.assert_can_view('oppia:cohort_add', self.staff_user)

    def test_student_cantview_add_cohort(self):
        self.assert_unauthorized('oppia:cohort_add', self.normal_user)

    # courses list view

    def test_anon_cantview_courses_list(self):
        self.assert_must_login('oppia:course')

    def test_admin_canview_courses_list(self):
        res = self.assert_can_view('oppia:course', self.admin_user)
        # check that the number of courses include the draft ones
        self.assertEqual(4, res.context['page'].paginator.count)

    def test_staff_cantview_courses_list(self):
        res = self.assert_can_view('oppia:course', self.staff_user)
        # check that the number of courses include the draft ones
        self.assertEqual(4, res.context['page'].paginator.count)

    def test_student_cantview_courses_list(self):
        self.assert_unauthorized('oppia:course', self.normal_user)

    # View course recent activity

    def test_anon_cantview_course_activity(self):
        self.assert_must_login('oppia:recent_activity',
                               view_kwargs={'course_id': 1})

    def test_view_nonexisting_course_activity(self):
        self.assert_not_found('oppia:recent_activity',
                              self.admin_user,
                              view_kwargs={'course_id': 1000})

    def test_admin_canview_course_activity(self):
        self.assert_can_view('oppia:recent_activity',
                             self.admin_user,
                             view_kwargs={'course_id': 1})

    def test_staff_canview_course_activity(self):
        self.assert_can_view('oppia:recent_activity',
                             self.staff_user,
                             view_kwargs={'course_id': 1})

    def test_student_canview_course_activity(self):
        self.assert_unauthorized('oppia:recent_activity',
                                 self.normal_user,
                                 view_kwargs={'course_id': 1})
    # TODO: Teacher view course activity for courses assigned to

    # View student activity (all activity)

    def test_anon_cantview_user_activity(self):
        self.assert_must_login('profile:user_activity',
                               view_kwargs={'user_id': 1})

    def test_view_nonexisting_user_activity(self):
        self.assert_not_found('profile:user_activity',
                              self.admin_user,
                              view_kwargs={'user_id': 1000})

    def test_admin_canview_user_activity(self):
        self.assert_can_view('profile:user_activity',
                             self.admin_user,
                             view_kwargs={'user_id': 1})

    def test_staff_canview_user_activity(self):
        self.assert_can_view('profile:user_activity',
                             self.staff_user,
                             view_kwargs={'user_id': 1})

    def test_student_cantview_user_activity(self):
        self.assert_unauthorized('profile:user_activity',
                                 self.normal_user,
                                 view_kwargs={'user_id': 1})

    def test_student_canview_self_activity(self):
        self.assert_can_view('profile:user_activity',
                             self.normal_user,
                             view_kwargs={'user_id': 2})
    # @TODO: Teacher view user activity of a user in a cohort he is assigned

    # View student activity (for a course)

    def test_anon_cantview_user_course_activity(self):
        self.assert_must_login('profile:user_course_activity',
                               view_kwargs={'course_id': 1, 'user_id': 1})

    def test_view_nonexisting_user_course_activity(self):
        self.assert_not_found('profile:user_course_activity', self.admin_user,
                              view_kwargs={'course_id': 1000,
                                           'user_id': 1000})

    def test_admin_canview_user_course_activity(self):
        self.assert_can_view('profile:user_course_activity',
                             self.admin_user,
                             view_kwargs={'course_id': 1, 'user_id': 1})

    def test_staff_canview_user_course_activity(self):
        self.assert_can_view('profile:user_course_activity',
                             self.staff_user,
                             view_kwargs={'course_id': 1, 'user_id': 1})

    def test_student_cantview_user_course_activity(self):
        self.assert_unauthorized('profile:user_course_activity',
                                 self.normal_user,
                                 view_kwargs={'course_id': 1, 'user_id': 1})

    def test_student_canview_self_course_activity(self):
        self.assert_can_view('profile:user_course_activity',
                             self.normal_user,
                             view_kwargs={'course_id': 1, 'user_id': 2})

    # Test is_manager permissions

    def test_is_manager_admin(self):
        self.assertFalse(is_manager_only(self.admin_user))

    def test_is_manager_staff(self):
        self.assertFalse(is_manager_only(self.staff_user))

    def test_is_manager_teacher(self):
        self.assertFalse(is_manager_only(self.teacher_user))

    def test_is_manager_user(self):
        self.assertFalse(is_manager_only(self.normal_user))

    def test_is_manager_viewer(self):
        self.assertFalse(is_manager_only(self.viewer_user))

    def test_is_manager_manager(self):
        self.assertTrue(is_manager_only(self.manager_user))
