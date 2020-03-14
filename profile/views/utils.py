import datetime

from django import forms
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from django.urls import reverse

from oppia.models import Tracker

STR_DATE_FORMAT = "%d %b %Y"


def filter_redirect(request_content):
    redirection = request_content.get('next')
    # Avoid redirecting to logout after login
    if redirection == reverse('profile:logout'):
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
                       .annotate(day=TruncDay('tracker_date'),
                                 month=TruncMonth('tracker_date'),
                                 year=TruncYear('tracker_date')) \
                       .values('day') \
                       .annotate(count=Count('id'))

    for i in range(0, no_days, +1):
        temp = start_date + datetime.timedelta(days=i)
        temp_date = temp.date().strftime(STR_DATE_FORMAT)
        count = next((dct['count']
                     for dct in trackers
                     if dct['day'].strftime(STR_DATE_FORMAT) == temp_date), 0)
        activity.append([temp_date, count])

    return activity
