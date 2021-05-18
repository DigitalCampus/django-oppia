from django.conf.urls import url
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string

from oppia.models import Points, Award, Tracker
from profile.views.user import ExportDataView
from quiz.models import QuizAttempt, QuizAttemptResponse

from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash


class DownloadDataResource(ModelResource):

    STR_CONTENT_TYPE = 'text/html'

    class Meta:
        queryset = User.objects.filter(pk=0)
        resource_name = 'downloaddata'
        allowed_methods = ['get']
        fields = []
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        always_return_data = False
        include_resource_uri = False

    def prepend_urls(self):
        return [
            # for profile
            url(r"^(?P<resource_name>%s)/profile%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('download_profile_data'),
                name="api_download_profile_data"),
            # for trackers
            url(r"^(?P<resource_name>%s)/activity%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('download_activity_data'),
                name="api_download_activity_data"),
            # for quiz
            url(r"^(?P<resource_name>%s)/quiz%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('download_quiz_data'),
                name="api_download_quiz_data"),
            # for badges
            url(r"^(?P<resource_name>%s)/badges%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('download_badge_data'),
                name="api_download_badge_data"),
            # for points
            url(r"^(?P<resource_name>%s)/points%s$"
                % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('download_points_data'),
                name="api_download_points_data"),
        ]

    # prevent just getting list of users
    def get_object_list(self, request):
        raise BadRequest()

    # prevent getting individual userid
    def get_object(self, request):
        raise BadRequest()

    def download_profile_data(self, request, **kwargs):
        self.is_authenticated(request)
        self.throttle_check(request)
        profile, additional_profile, custom_profile = \
            ExportDataView.get_profile_data(request.user)
        response_data = render_to_string('profile/export/profile.html',
                                         {'profile': profile,
                                          'additional_profile':
                                          additional_profile,
                                          'custom_profile': custom_profile})
        response = HttpResponse(response_data,
                                content_type=self.STR_CONTENT_TYPE)
        response['Content-Disposition'] = \
            'attachment; filename="%s-profile.html"' % (request.user.username)
        return response

    def download_activity_data(self, request, **kwargs):
        self.is_authenticated(request)
        self.throttle_check(request)
        my_activity = Tracker.objects.filter(user=request.user)
        response_data = render_to_string('profile/export/activity.html',
                                         {'activity': my_activity})
        response = HttpResponse(response_data,
                                content_type=self.STR_CONTENT_TYPE)
        response['Content-Disposition'] = \
            'attachment; filename="%s-activity.html"' % (request.user.username)
        return response

    def download_quiz_data(self, request, **kwargs):
        self.is_authenticated(request)
        self.throttle_check(request)
        my_quizzes = []
        my_quiz_attempts = QuizAttempt.objects.filter(user=request.user)
        for mqa in my_quiz_attempts:
            data = {}
            data['quizattempt'] = mqa
            data['quizattemptresponses'] = QuizAttemptResponse.objects \
                .filter(quizattempt=mqa)
            my_quizzes.append(data)
        response_data = render_to_string('profile/export/quiz_attempts.html',
                                         {'quiz_attempts': my_quizzes})
        response = HttpResponse(response_data,
                                content_type=self.STR_CONTENT_TYPE)
        response['Content-Disposition'] = \
            'attachment; filename="%s-quizzes.html"' % (request.user.username)
        return response

    def download_badge_data(self, request, **kwargs):
        self.is_authenticated(request)
        self.throttle_check(request)
        badges = Award.objects.filter(user=request.user)
        response_data = render_to_string('profile/export/badges.html',
                                         {'badges': badges})
        response = HttpResponse(response_data,
                                content_type=self.STR_CONTENT_TYPE)
        response['Content-Disposition'] = \
            'attachment; filename="%s-badges.html"' % (request.user.username)
        return response

    def download_points_data(self, request, **kwargs):
        self.is_authenticated(request)
        self.throttle_check(request)
        points = Points.objects.filter(user=request.user)
        response_data = render_to_string('profile/export/points.html',
                                         {'points': points})
        response = HttpResponse(response_data,
                                content_type=self.STR_CONTENT_TYPE)
        response['Content-Disposition'] = \
            'attachment; filename="%s-points.html"' % (request.user.username)

        return response
