from django.urls import reverse
from django.test import TestCase


class PermissionsViewTest(TestCase):
    fixtures = ['user.json', 'oppia.json', 'quiz.json', 'permissions.json']

    def setUp(self):
        super(PermissionsViewTest, self).setUp()
        self.login_url = reverse('profile_login')
        self.admin_user = {
            'user': 'admin',
            'password': 'password'
        }
        self.staff_user = {
            'user': 'staff',
            'password': 'password'
        }
        self.normal_user = {
            'user': 'demo',
            'password': 'password'
        }
        self.teacher_user = {
            'user': 'teacher',
            'password': 'password'
        }

    def get_view(self, route, user=None):
        if user is not None:
            self.client.login(username=user['user'], password=user['password'])
        return self.client.get(route)

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
    # Permissions tests (based on http://oppiamobile.readthedocs.io/en/latest/permissions/server.html)

    ############ Django admin #############

    def test_anon_cantview_admin(self):
        self.assert_must_login('admin:index')

    def test_admin_canview_admin(self):
        self.assert_can_view('admin:index', self.admin_user)

    def test_staff_cantview_admin(self):
        self.assert_can_view('admin:index', self.staff_user)

    def test_student_cantview_admin(self):
        # Check that gets redirected to admin login
        route = reverse('admin:index')
        res = self.get_view(route, self.normal_user)
        self.assertRedirects(res, route + 'login/?next=' + route)
    ############ Upload courses view #############

    def test_anon_cantview_upload_courses(self):
        self.assert_must_login('oppia_upload')

    def test_admin_canview_upload_courses(self):
        self.assert_can_view('oppia_upload', self.admin_user)

    def test_staff_canview_upload_courses(self):
        self.assert_can_view('oppia_upload', self.staff_user)

    def test_student_cantview_upload_courses(self):
        self.assert_unauthorized('oppia_upload', self.normal_user)

    def test_user_with_canupload_canview_upload_courses(self):
        self.assert_can_view('oppia_upload', self.teacher_user)
    ############ Bulk upload users view #############

    def test_anon_cantview_bulk_upload(self):
        self.assert_must_login('profile_upload')

    def test_admin_canview_bulk_upload(self):
        self.assert_can_view('profile_upload', self.admin_user)

    def test_staff_cantview_bulk_upload(self):
        self.assert_unauthorized('profile_upload', self.staff_user)

    def test_student_cantview_bulk_upload(self):
        self.assert_unauthorized('profile_upload', self.normal_user)
    ############ View cohort list #############

    def test_anon_cantview_cohorts(self):
        self.assert_must_login('oppia_cohorts')

    def test_admin_canview_cohorts(self):
        self.assert_can_view('oppia_cohorts', self.admin_user)

    def test_staff_canview_cohorts(self):
        self.assert_can_view('oppia_cohorts', self.staff_user)

    def test_student_cantview_cohorts(self):
        self.assert_unauthorized('oppia_cohorts', self.normal_user)
    # TODO: Define a teacher user to test cohort management

    ############ View a cohort ################

    def test_anon_cantview_cohort(self):
        self.assert_must_login('oppia_cohort_view', view_kwargs={'cohort_id': 1})

    def test_view_nonexisting_cohort(self):
        self.assert_not_found('oppia_cohort_view', self.admin_user, view_kwargs={'cohort_id': 1000})

    def test_admin_canview_cohort(self):
        self.assert_can_view('oppia_cohort_view', self.admin_user, view_kwargs={'cohort_id': 1})

    def test_staff_canview_cohort(self):
        self.assert_can_view('oppia_cohort_view', self.staff_user, view_kwargs={'cohort_id': 1})

    def test_student_cantview_cohort(self):
        self.assert_unauthorized('oppia_cohort_view', self.normal_user, view_kwargs={'cohort_id': 1})
    # TODO: Teacher view cohort s/he is assigned into

    ############ View a cohort course activity ################

    def test_anon_cantview_cohort_course(self):
        self.assert_must_login('oppia_cohort_course_view', view_kwargs={'cohort_id': 1, 'course_id': 1})

    def test_view_nonexisting_cohort_course(self):
        self.assert_not_found('oppia_cohort_course_view', self.admin_user,
                              view_kwargs={'cohort_id': 1000, 'course_id': 1000})

    def test_admin_canview_cohort_course(self):
        self.assert_can_view('oppia_cohort_course_view', self.admin_user, view_kwargs={'cohort_id': 1, 'course_id': 1})

    def test_staff_canview_cohort_course(self):
        self.assert_can_view('oppia_cohort_course_view', self.staff_user, view_kwargs={'cohort_id': 1, 'course_id': 1})

    def test_student_cantview_cohort_course(self):
        self.assert_unauthorized('oppia_cohort_course_view', self.normal_user,
                                view_kwargs={'cohort_id': 1, 'course_id': 1})
    # TODO: Teacher view cohort s/he is assigned into

    ############ Add new cohort #############

    def test_anon_cantview_add_cohort(self):
        self.assert_must_login('oppia_cohort_add')

    def test_admin_canview_add_cohort(self):
        self.assert_can_view('oppia_cohort_add', self.admin_user)

    def test_staff_canview_add_cohort(self):
        self.assert_can_view('oppia_cohort_add', self.staff_user)

    def test_student_cantview_add_cohort(self):
        self.assert_unauthorized('oppia_cohort_add', self.normal_user)
    ############ courses list view #############

    def test_anon_cantview_courses_list(self):
        self.assert_must_login('oppia_course')

    def test_admin_canview_courses_list(self):
        res = self.assert_can_view('oppia_course', self.admin_user)
        # check that the number of courses include the draft ones
        self.assertEqual(res.context['page'].paginator.count, 3)

    def test_staff_cantview_courses_list(self):
        res = self.assert_can_view('oppia_course', self.staff_user)
        # check that the number of courses include the draft ones
        self.assertEqual(res.context['page'].paginator.count, 3)

    def test_student_cantview_courses_list(self):
        res = self.assert_can_view('oppia_course', self.normal_user)
        # check that the number of courses dont include the draft ones
        self.assertEqual(res.context['page'].paginator.count, 2)
    ############ View course recent activity #############

    def test_anon_cantview_course_activity(self):
        self.assert_must_login('oppia_recent_activity', view_kwargs={'course_id': 1})

    def test_view_nonexisting_course_activity(self):
        self.assert_not_found('oppia_recent_activity', self.admin_user, view_kwargs={'course_id': 1000})

    def test_admin_canview_course_activity(self):
        self.assert_can_view('oppia_recent_activity', self.admin_user, view_kwargs={'course_id': 1})

    def test_staff_canview_course_activity(self):
        self.assert_can_view('oppia_recent_activity', self.staff_user, view_kwargs={'course_id': 1})

    def test_student_canview_course_activity(self):
        self.assert_unauthorized('oppia_recent_activity', self.normal_user, view_kwargs={'course_id': 1})
    # TODO: Teacher view course activity for courses assigned to

    ############ View student activity (all activity) #####

    def test_anon_cantview_user_activity(self):
        self.assert_must_login('profile_user_activity', view_kwargs={'user_id': 1})

    def test_view_nonexisting_user_activity(self):
        self.assert_not_found('profile_user_activity', self.admin_user, view_kwargs={'user_id': 1000})

    def test_admin_canview_user_activity(self):
        self.assert_can_view('profile_user_activity', self.admin_user, view_kwargs={'user_id': 1})

    def test_staff_canview_user_activity(self):
        self.assert_can_view('profile_user_activity', self.staff_user, view_kwargs={'user_id': 1})

    def test_student_cantview_user_activity(self):
        self.assert_unauthorized('profile_user_activity', self.normal_user, view_kwargs={'user_id': 1})

    def test_student_canview_self_activity(self):
        self.assert_can_view('profile_user_activity', self.normal_user, view_kwargs={'user_id': 2})
    # @TODO: Teacher view user activity of a user in a cohort he is assigned

    ############ View student activity (for a course) #####

    def test_anon_cantview_user_course_activity(self):
        self.assert_must_login('profile_user_course_activity', view_kwargs={'course_id': 1, 'user_id': 1})

    def test_view_nonexisting_user_course_activity(self):
        self.assert_not_found('profile_user_course_activity', self.admin_user,
                              view_kwargs={'course_id': 1000, 'user_id': 1000})

    def test_admin_canview_user_course_activity(self):
        self.assert_can_view('profile_user_course_activity', self.admin_user,
                             view_kwargs={'course_id': 1, 'user_id': 1})

    def test_staff_canview_user_course_activity(self):
        self.assert_can_view('profile_user_course_activity', self.staff_user,
                             view_kwargs={'course_id': 1, 'user_id': 1})

    def test_student_cantview_user_course_activity(self):
        self.assert_unauthorized('profile_user_course_activity', self.normal_user,
                                view_kwargs={'course_id': 1, 'user_id': 1})

    def test_student_canview_self_course_activity(self):
        self.assert_can_view('profile_user_course_activity', self.normal_user,
                             view_kwargs={'course_id': 1, 'user_id': 2})
    # TODO: Teacher view user activity of a user in a cohort he is assigned

    ############ analytics summary overview #############

    def test_anon_cantview_summary_overview(self):
        self.assert_must_login('oppia_viz_summary')

    def test_admin_canview_summary_overview(self):
        self.assert_can_view('oppia_viz_summary', self.admin_user)

    def test_staff_canview_summary_overview(self):
        self.assert_can_view('oppia_viz_summary', self.staff_user)

    def test_student_cantview_summary_overview(self):
        self.assert_unauthorized('oppia_viz_summary', self.normal_user)
