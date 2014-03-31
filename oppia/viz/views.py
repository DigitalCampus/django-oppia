# oppia/viz/views.py

import datetime
import json
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count, Sum, Q

from django.contrib.auth import (authenticate, logout, views)
from django.contrib.auth.models import User

from oppia.models import CourseDownload, Tracker, Course
from oppia.viz.models import UserLocationVisualization


def summary_view(request):
    if not request.user.is_staff:
         raise Http404
    # User registrations
    user_registrations = User.objects.\
                        extra(select={'month':'extract( month from date_joined )',
                                      'year':'extract( year from date_joined )'}).\
                        values('month','year').\
                        annotate(count=Count('id')).order_by('year','month')
    
    # Countries
    hits_by_country =  UserLocationVisualization.objects.all().values('country_code','country_name').annotate(country_total_hits=Sum('hits')).order_by('-country_total_hits')
    total_hits = UserLocationVisualization.objects.all().aggregate(total_hits=Sum('hits'))
    total_countries = hits_by_country.count()
    
    i = 0
    country_activity = []
    other_country_activity = 0
    for c in hits_by_country:
        if i < 20:
            hits_percent = float(c['country_total_hits'] * 100.0/total_hits['total_hits'])
            country_activity.append({'country_code':c['country_code'],'country_name':c['country_name'],'hits_percent':hits_percent })
        else:
            other_country_activity += c['country_total_hits']
        i += 1
    if i > 20:
        hits_percent = float(other_country_activity * 100.0/total_hits['total_hits'])
        country_activity.append({'country_code':None,'country_name':_('Other'),'hits_percent':hits_percent })
        
    # Language
    hit_by_language = Tracker.objects.filter(user__is_staff=False).exclude(lang=None).values('lang').annotate(total_hits=Count('id')).order_by('-total_hits')
    total_hits = Tracker.objects.filter(user__is_staff=False).exclude(lang=None).aggregate(total_hits=Count('id'))
    
    i = 0
    languages = []
    other_languages = 0
    for hbl in hit_by_language:
        if i < 10:
            hits_percent = float(hbl['total_hits'] * 100.0/total_hits['total_hits'])
            languages.append({'lang':hbl['lang'],'hits_percent':hits_percent })
        else:
            other_languages += hbl['total_hits']
        i += 1
    if i > 10:
        hits_percent = float(other_languages * 100.0/total_hits['total_hits'])
        languages.append({'lang':_('Other'),'hits_percent':hits_percent })
        
    # Course Downloads
    course_downloads = CourseDownload.objects.filter(user__is_staff=False).\
                        extra(select={'month':'extract( month from download_date )',
                                      'year':'extract( year from download_date )'}).\
                        values('month','year').\
                        annotate(count=Count('id')).order_by('year','month')
    
    # Course Activity
    course_activity = Tracker.objects.filter(user__is_staff=False).\
                        extra(select={'month':'extract( month from submitted_date )',
                                      'year':'extract( year from submitted_date )'}).\
                        values('month','year').\
                        annotate(count=Count('id')).order_by('year','month')
                        
    last_month = datetime.datetime.now() - datetime.timedelta(days=31)
    hit_by_course = Tracker.objects.filter(user__is_staff=False, submitted_date__gte=last_month).exclude(course_id=None).values('course_id').annotate(total_hits=Count('id')).order_by('-total_hits')
    total_hits = Tracker.objects.filter(user__is_staff=False, submitted_date__gte=last_month).exclude(course_id=None).aggregate(total_hits=Count('id'))
    
    i = 0
    hot_courses = []
    other_course_activity = 0
    for hbc in hit_by_course:
        if i < 10:
            hits_percent = float(hbc['total_hits'] * 100.0/total_hits['total_hits'])
            course = Course.objects.get(id=hbc['course_id'])
            hot_courses.append({'course':course,'hits_percent':hits_percent })
        else:
            other_course_activity += hbc['total_hits']
        i += 1
    if i > 10:
        hits_percent = float(other_course_activity * 100.0/total_hits['total_hits'])
        hot_courses.append({'course':_('Other'),'hits_percent':hits_percent })
                       
    return render_to_response('oppia/viz/summary.html',
                              {'user_registrations': user_registrations,
                               'total_countries': total_countries,
                               'country_activity': country_activity,
                               'languages': languages,
                               'course_downloads': course_downloads,
                               'course_activity': course_activity, 
                               'hot_courses': hot_courses, }, 
                              context_instance=RequestContext(request))

def map_view(request):
    return render_to_response('oppia/viz/map.html', 
                              context_instance=RequestContext(request))