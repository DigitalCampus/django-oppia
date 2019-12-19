
from django.urls import reverse
from oppia.test import OppiaTestCase


class PermissionsViewTest(OppiaTestCase):

    def get_view(self, route, user=None):
        if user is not None:
            self.client.force_login(user)
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

    # upload media file
    def test_anon_cantview_av_upload(self):
        self.assert_must_login('oppia_av_upload')

    def test_admin_canview_av_upload(self):
        self.assert_can_view('oppia_av_upload', self.admin_user)

    def test_staff_canview_av_upload(self):
        self.assert_can_view('oppia_av_upload', self.staff_user)

    def test_student_cantview_av_upload(self):
        self.assert_unauthorized('oppia_av_upload', self.normal_user)

    def test_teacher_canview_av_upload(self):
        # since has can_upload set in profile
        self.assert_can_view('oppia_av_upload', self.teacher_user)
