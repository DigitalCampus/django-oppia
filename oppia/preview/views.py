# oppia/preview/views.py

from django.conf import settings
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from oppia.models import Course
from oppia.views import check_can_view
from oppia.course_xml_reader import CourseXML

def home_view(request):
    
    if request.user.is_staff:
        course_list = Course.objects.filter(is_archived=False).order_by('title')
    else:
        course_list = Course.objects.filter(is_draft=False,is_archived=False).order_by('title') 
        
    return render_to_response('oppia/preview/home.html',
                              {'course_list': course_list}, 
                              context_instance=RequestContext(request))

def course_home_view(request, id):
    course = check_can_view(request, id)
    
    course_xml = CourseXML(settings.MEDIA_ROOT + "courses/" + course.shortname + "/module.xml")
    return render_to_response('oppia/preview/course_home.html',
                              {'course': course, 'course_structure': course_xml}, 
                              context_instance=RequestContext(request))