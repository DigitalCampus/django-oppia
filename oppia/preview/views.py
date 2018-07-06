# oppia/preview/views.py
import codecs
import os
import oppia
import re

from django.conf import settings
from django.shortcuts import render
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from oppia.models import Course, Activity, Tracker
from oppia.permissions import can_view_course
from oppia.course_xml_reader import CourseXML


def home_view(request):

    course_list = []
    # only get courses that are already published for preview
    for dir in os.listdir(settings.MEDIA_ROOT + "courses/"):
        try:
            if request.user.is_staff:
                course = Course.objects.get(is_archived=False, shortname=dir)
            else:
                course = Course.objects.get(is_draft=False, is_archived=False, shortname=dir)
            course_list.append(course)
        except Course.DoesNotExist:
            pass

    return render(request, 'oppia/preview/home.html',
                              {'course_list': course_list})


def course_home_view(request, id):
    course = can_view_course(request, id)
    return render(request, 'oppia/preview/course_home.html',
                              {'course': course})


def course_activity_view(request, course_id, activity_id):
    course = can_view_course(request, course_id)
    activity = Activity.objects.get(pk=activity_id)

    # log the activity in the tracker
    tracker = Tracker()
    tracker.user = request.user
    tracker.course = course
    tracker.type = activity.type
    tracker.data = ""
    tracker.ip = request.META.get('REMOTE_ADDR', oppia.DEFAULT_IP_ADDRESS)
    tracker.agent = request.META.get('HTTP_USER_AGENT', 'unknown')
    tracker.activity_title = activity.title
    tracker.section_title = activity.section.title
    tracker.save()

    if activity.type == "page":
        activity_content_file = activity.get_content()

        with codecs.open(settings.MEDIA_ROOT + "courses/" + course.shortname + "/" + activity_content_file, "r", "utf-8") as f:
            s = f.read()

        template = re.compile('\<body(?P<body>.*?)>(?P<content>.*)\<\/body\>', re.DOTALL)

        activity_content = template.search(s).group('content')
        activity_content = activity_content.replace("images/", settings.MEDIA_URL + "courses/" + course.shortname + "/images/")

        return render(request, 'oppia/preview/course_activity_page.html',
                                  {'course': course, 'activity': activity, 'content': activity_content})
    else:
        activity_content = None
        return render(request, 'oppia/preview/course_activity_not_supported.html',
                                  {'course': course, 'activity': activity, 'content': activity_content})
