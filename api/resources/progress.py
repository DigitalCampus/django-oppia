from django.conf.urls import url
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse, JsonResponse, Http404
from django.utils.translation import ugettext_lazy as _

from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.exceptions import BadRequest, Unauthorized
from tastypie.resources import ModelResource
from tastypie.utils import timezone

from oppia import permissions
from oppia.models import Course, Participant
from summary.models import UserCourseSummary

STR_USER_NOT_FOUND = _(u"User not found or unauthorised")

class UserCourseSummaryResource(ModelResource):

    class Meta:
        queryset = UserCourseSummary.objects.all()
        allowed_methods = ['get']
        fields = []
        resource_name = 'progress'
        include_resource_uri = False
        authentication = ApiKeyAuthentication()
        authorization = ReadOnlyAuthorization()
        always_return_data = True

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<username>\w[\w/-]*)/$"
                % (self._meta.resource_name),
                self.wrap_view('user_course_progress'),
                name="user_course_progress")
            ]
     
    def get_user(self, request, **kwargs):
        self.is_authenticated(request)
        self.throttle_check(request)

        username = kwargs.pop('username', None)
        if request.user.is_staff or (request.user.username == username):
            try:
                user = User.objects.get(username=username)
                return user
            except User.DoesNotExist:
                raise Http404(STR_USER_NOT_FOUND)
        else:
            try:
                view_user = User.objects.get(username=username)
                courses = Course.objects.filter(
                    coursecohort__cohort__participant__user=view_user,
                    coursecohort__cohort__participant__role=Participant.STUDENT) \
                    .filter(
                        coursecohort__cohort__participant__user=request.user,
                        coursecohort__cohort__participant__role=Participant.TEACHER) \
                    .count()
                if courses > 0:
                    return view_user
                else:
                    raise Http404(STR_USER_NOT_FOUND)
            except User.DoesNotExist:
                raise Http404(STR_USER_NOT_FOUND)
    
    def get_object_list(self, request):
        raise BadRequest(_("Please specify a user"))
    
    def user_course_progress(self, request, **kwargs): 
        user = self.get_user(request, **kwargs)
        
        cc, oc, ac = permissions.get_user_courses(request, user)
        
        if request.user.is_staff or (request.user == user):
            ucs_qs = UserCourseSummary.objects.filter(user=user).order_by('course__shortname')
        else:
            ucs_qs = UserCourseSummary.objects.filter(user=user, course__in=ac).order_by('course__shortname')
        
        courses = []
        for ucs in ucs_qs:
            percent_complete = (ucs.completed_activities / 
                                ucs.course.get_no_activities()) * 100
            c = {}
            c['shortname'] = ucs.course.shortname
            c['title'] = ucs.course.title
            c['points'] = ucs.points
            c['total_activity'] = ucs.total_activity
            c['quizzes_passed'] = ucs.quizzes_passed
            c['badges_achieved'] = ucs.badges_achieved
            c['media_viewed'] = ucs.media_viewed
            c['completed_activities'] = ucs.completed_activities
            c['percent_complete'] = int(percent_complete)
            courses.append(c)

        return JsonResponse(courses, safe=False)
          
