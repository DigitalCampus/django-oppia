from oppia.test import OppiaTestCase
from django.urls import reverse


class PermissionsViewTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_course_permissions.json']

    def assert_response(self, view, status_code, user=None, view_kwargs=None):
        route = reverse(view, kwargs=view_kwargs)
        res = self.get_view(route, user)
        self.assertEqual(res.status_code, status_code)
        return res

    def assert_can_view(self, view, user=None, view_kwargs=None):
        return self.assert_response(view, 200, user, view_kwargs)

    def assert_cannot_view(self, view, user=None, view_kwargs=None):
        return self.assert_response(view, 401, user, view_kwargs)

    def assert_unauthorized(self, view, user=None, view_kwargs=None):
        return self.assert_response(view, 403, user, view_kwargs)

    def assert_must_login(self, view, user=None, view_kwargs=None):
        route = reverse(view, kwargs=view_kwargs)
        res = self.get_view(route, user)
        login_url = self.login_url + '?next=' + route
        self.assertRedirects(res, login_url)
        return res

    # upload activity log file
    def test_anon_cantview_av_upload(self):
        self.assert_must_login('activitylog:upload')

    def test_admin_canview_av_upload(self):
        self.assert_can_view('activitylog:upload', self.admin_user)

    def test_staff_canview_av_upload(self):
        self.assert_can_view('activitylog:upload', self.staff_user)

    def test_teacher_cantview_av_upload(self):
        self.assert_can_view('activitylog:upload', self.teacher_user)

    def test_student_cantview_av_upload(self):
        self.assert_unauthorized('activitylog:upload', self.normal_user)
