from django.test import TestCase

from tests.utils import *

from tests.user_logins import *

class PermissionsViewTest(TestCase):
    fixtures = ['tests/test_user.json', 
                'tests/test_oppia.json', 
                'tests/test_quiz.json', 
                'tests/test_permissions.json']

    def setUp(self):
        super(PermissionsViewTest, self).setUp()
        self.login_url = reverse('profile_login')

    def get_view(self, route, user=None):
        if user is not None:
            self.client.login(username=user['user'], password=user['password'])
        return self.client.get(route)

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

    ############ upload activity log file #############
    def test_anon_cantview_av_upload(self):
        self.assert_must_login('oppia_activitylog_upload')

    def test_admin_canview_av_upload(self):
        self.assert_can_view('oppia_activitylog_upload', ADMIN_USER)

    def test_staff_canview_av_upload(self):
        self.assert_can_view('oppia_activitylog_upload', STAFF_USER)

    def test_student_cantview_av_upload(self):
        self.assert_unauthorized('oppia_activitylog_upload', NORMAL_USER)
