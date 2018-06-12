# oppia/viz/views.py

import datetime
import json

from django.contrib.auth import authenticate, logout, views
from django.contrib.auth.models import User
from django.core import exceptions
from django.db.models import Count, Sum, Q
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from oppia.forms import DateDiffForm
from oppia.models import Tracker, Course
from oppia.summary.models import CourseDailyStats
from oppia.viz.models import UserLocationVisualization


def summary_view(request):
    if not request.user.is_staff:
        raise exceptions.PermissionDenied

    start_date = timezone.now() - datetime.timedelta(days=365)
    if request.method == 'POST':
        form = DateDiffForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get("start_date")
    else:
        data = {}
        data['start_date'] = start_date
        form = DateDiffForm(initial=data)

    # User registrations
    user_registrations = User.objects.filter(date_joined__gte=start_date). \
                        extra(select={'month': 'extract( month from date_joined )',
                                      'year': 'extract( year from date_joined )'}). \
                        values('month', 'year'). \
                        annotate(count=Count('id')).order_by('year', 'month')

    previous_user_registrations = User.objects.filter(date_joined__lt=start_date).count()

    # Countries
    hits_by_country = UserLocationVisualization.objects.all().values('country_code', 'country_name').annotate(country_total_hits=Sum('hits')).order_by('-country_total_hits')
    total_hits = UserLocationVisualization.objects.all().aggregate(total_hits=Sum('hits'))
    total_countries = hits_by_country.count()

    i = 0
    country_activity = []
    other_country_activity = 0
    for c in hits_by_country:
        if i < 20:
            hits_percent = float(c['country_total_hits'] * 100.0 / total_hits['total_hits'])
            country_activity.append({'country_code': c['country_code'], 'country_name': c['country_name'], 'hits_percent': hits_percent})
        else:
            other_country_activity += c['country_total_hits']
        i += 1
    if i > 20:
        hits_percent = float(other_country_activity * 100.0 / total_hits['total_hits'])
        country_activity.append({'country_code': None, 'country_name': _('Other'), 'hits_percent': hits_percent})

    # Language
    hit_by_language = Tracker.objects.filter(user__is_staff=False).exclude(lang=None).values('lang').annotate(total_hits=Count('id')).order_by('-total_hits')
    total_hits = Tracker.objects.filter(user__is_staff=False).exclude(lang=None).aggregate(total_hits=Count('id'))

    i = 0
    languages = []
    other_languages = 0
    for hbl in hit_by_language:
        if i < 10:
            hits_percent = float(hbl['total_hits'] * 100.0 / total_hits['total_hits'])
            languages.append({'lang': hbl['lang'], 'hits_percent': hits_percent})
        else:
            other_languages += hbl['total_hits']
        i += 1
    if i > 10:
        hits_percent = float(other_languages * 100.0 / total_hits['total_hits'])
        languages.append({'lang': _('Other'), 'hits_percent': hits_percent})

    # Course Downloads
    course_downloads = CourseDailyStats.objects.filter(day__gte=start_date, type='download') \
                        .extra({'month': 'month(day)', 'year': 'year(day)'}) \
                        .values('month', 'year') \
                        .annotate(count=Sum('total')) \
                        .order_by('year', 'month')
    previous_course_downloads = CourseDailyStats.objects.filter(day__lt=start_date, type='download').aggregate(total=Sum('total')).get('total', 0)
    if previous_course_downloads is None:
        previous_course_downloads = 0

    # Course Activity
    course_activity = CourseDailyStats.objects.filter(day__gte=start_date) \
                        .extra({'month': 'month(day)', 'year': 'year(day)'}) \
                        .values('month', 'year') \
                        .annotate(count=Sum('total')) \
                        .order_by('year', 'month')

    previous_course_activity = CourseDailyStats.objects.filter(day__lt=start_date).aggregate(total=Sum('total')).get('total', 0)
    if previous_course_activity is None:
        previous_course_activity = 0

    last_month = timezone.now() - datetime.timedelta(days=131)
    
    hit_by_course = CourseDailyStats.objects \
                        .filter(day__gte=last_month, course__isnull=False).values('course_id') \
                        .annotate(total_hits=Sum('total')).order_by('-total_hits')
    total_hits = sum(cstats['total_hits'] for cstats in hit_by_course)

    i = 0
    hot_courses = []
    other_course_activity = 0
    for hbc in hit_by_course:
        if i < 10:
            hits_percent = float(hbc['total_hits'] * 100.0 / total_hits)
            course = Course.objects.get(id=hbc['course_id'])
            hot_courses.append({'course': course, 'hits_percent': hits_percent})
        else:
            other_course_activity += hbc['total_hits']
        i += 1
    if i > 10:
        hits_percent = float(other_course_activity * 100.0 / total_hits)
        hot_courses.append({'course': _('Other'), 'hits_percent': hits_percent})

    searches = CourseDailyStats.objects.filter(day__gte=start_date, type='search') \
                        .extra({'month': 'month(day)', 'year': 'year(day)'}) \
                        .values('month', 'year') \
                        .annotate(count=Sum('total')) \
                        .order_by('year', 'month')

    previous_searches = CourseDailyStats.objects.filter(day__lt=start_date, type='search').aggregate(total=Sum('total')).get('total', 0)
    if previous_searches is None:
        previous_searches = 0

    return render(request, 'oppia/viz/summary.html',
                              {'form': form,
                               'user_registrations': user_registrations,
                               'previous_user_registrations': previous_user_registrations,
                               'total_countries': total_countries,
                               'country_activity': country_activity,
                               'languages': languages,
                               'course_downloads': course_downloads,
                               'previous_course_downloads': previous_course_downloads,
                               'course_activity': course_activity,
                               'previous_course_activity': previous_course_activity,
                               'hot_courses': hot_courses,
                               'searches': searches,
                               'previous_searches': previous_searches, })


def map_view(request):
    return render(request, 'oppia/viz/map.html')
