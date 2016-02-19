# oppia/reports/views.py
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http.response import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from oppia.models import Course


def menu_reports(request):
    # add in here any reports that need to appear in the menu
    #return [{'name': 'test', 'url':'/reports/1/'},{'name': 'test2', 'url':'/reports/2/'}]
    return [{'name':'completion_rates', 'url':'/reports/completion_rates/'}]

from django.db.models.query import QuerySet
from pprint import PrettyPrinter

def completion_rates(request):

    courses, response = can_view_courses_list(request)
    if response is not None:
        return response

    courses_list = []
    for course in courses:
        obj = {}
        obj['course'] = course

    return render_to_response('oppia/reports/completion_rates.html',
                              {'courses_list': courses_list },
                              context_instance=RequestContext(request))

def can_view_courses_list(request):
    if not request.user.is_staff:
        return None, HttpResponse('Unauthorized', status=401)
    else:
        courses = Course.objects.filter(is_draft=False,is_archived=False).order_by('title')
    return courses, None