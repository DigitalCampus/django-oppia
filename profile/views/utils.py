import csv
import datetime
import operator
from itertools import chain

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import (authenticate, login)
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db import IntegrityError
from django.db.models import Count, Max, Min, Avg, Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _
from tastypie.models import ApiKey

import profile

from oppia import emailer
from oppia.models import Points, Award, Tracker, Activity
from oppia.permissions import get_user, \
                              get_user_courses, \
                              can_view_course, \
                              can_edit_user
from profile.forms import LoginForm, \
                          RegisterForm, \
                          ResetForm, \
                          ProfileForm, \
                          UploadProfileForm, \
                          UserSearchForm, \
                          DeleteAccountForm
from profile.models import UserProfile
from quiz.models import Quiz, QuizAttempt, QuizAttemptResponse
from reports.signals import dashboard_accessed
from settings import constants
from settings.models import SettingProperties
from summary.models import UserCourseSummary

def filter_redirect(request_content):
    redirection = request_content.get('next')
    # Avoid redirecting to logout after login
    if redirection == reverse('profile_logout'):
        return None
    else:
        return redirection


def get_paginated_users(request):
    default_order = 'date_joined'
    ordering = request.GET.get('order_by', None)
    if ordering is None:
        ordering = default_order

    users = User.objects.all().order_by(ordering)
    paginator = Paginator(users, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    return ordering, paginator.page(page)

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search
        fields.

    '''
    query = None  # Query to search in every field
    for field_name in search_fields:
        q = Q(** {"%s__icontains" % field_name: query_string})
        query = q if query is None else (query | q)

    return query


def get_filters_from_row(search_form):
    filters = {}
    for row in search_form.cleaned_data:
        if search_form.cleaned_data[row]:
            if row == 'start_date':
                filters['date_joined__gte'] = search_form.cleaned_data[row]
            elif row == 'end_date':
                filters['date_joined__lte'] = search_form.cleaned_data[row]
            elif isinstance(search_form.fields[row], forms.CharField):
                filters["%s__icontains" % row] = search_form.cleaned_data[row]
            else:
                filters[row] = search_form.cleaned_data[row]
    return filters


def get_tracker_activities(start_date,
                           end_date,
                           user,
                           course_ids=[],
                           course=None):
    activity = []
    no_days = (end_date - start_date).days + 1
    if course:
        trackers = Tracker.objects.filter(course=course)
    else:
        trackers = Tracker.objects.filter(course__id__in=course_ids)

    trackers = trackers.filter(user=user,
                               tracker_date__gte=start_date,
                               tracker_date__lte=end_date) \
                       .extra({'activity_date': "date(tracker_date)"}) \
                       .values('activity_date') \
                       .annotate(count=Count('id'))

    for i in range(0, no_days, +1):
        temp = start_date + datetime.timedelta(days=i)
        count = next((dct['count']
                      for dct in trackers
                      if dct['activity_date'] == temp.date()), 0)
        activity.append([temp.strftime("%d %b %Y"), count])

    return activity