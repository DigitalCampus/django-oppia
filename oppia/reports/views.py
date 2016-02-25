# oppia/reports/views.py
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from oppia.models import Course, Badge, Award, AwardCourse


def menu_reports(request):
    # add in here any reports that need to appear in the menu
    #return [{'name': 'test', 'url':'/reports/1/'},{'name': 'test2', 'url':'/reports/2/'}]
    return [{'name':_('Completion Rates'), 'url':reverse('oppia_completion_rates')}]

def completion_rates(request):

    courses, response = can_view_courses_list(request)
    if response is not None:
        return response

    courses_list = []
    for course in courses:
        obj = {}
        obj['course'] = course

        courseActivities = course.get_no_activities()
        no_users = User.objects.filter(tracker__course=course).distinct().count()

        awards_given = AwardCourse.objects.filter(course=course).count()

        obj['enroled'] = no_users
        if no_users > 0:
            obj['completion'] = (float(awards_given) / float(no_users)) * 100
        else:
            obj['completion'] = 0
            
        courses_list.append(obj)

    return render_to_response('oppia/reports/completion_rates.html',
                              {'courses_list': courses_list },
                              context_instance=RequestContext(request))

def course_completion_rates(request,course_id):

    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        raise Http404

    users_completed = []
    users_incompleted = []

    courseActivities = course.get_no_activities()
    users = User.objects.filter(tracker__course=course).distinct()
    for user in users:
        userActivities = Course.get_activities_completed(course, user)
        userObj = {'user': user}
        userObj['activities_completed'] = userActivities
        userObj['completion_percent'] = (userActivities * 100 / courseActivities)
        if (userActivities >= courseActivities):
            users_completed.append(userObj)
        else:
            users_incompleted.append(userObj)

    return render_to_response('oppia/reports/course_completion_rates.html',
                              {
                                  'course': course,
                                  'users_enroled_count': len(users_completed) + len(users_incompleted),
                                  'users_completed': users_completed,
                                  'users_incompleted': users_incompleted,
                              },
                              context_instance=RequestContext(request))

def can_view_courses_list(request):
    if not request.user.is_staff:
        return None, HttpResponse('Unauthorized', status=401)
    else:
        courses = Course.objects.filter(is_draft=False,is_archived=False).order_by('title')
    return courses, None