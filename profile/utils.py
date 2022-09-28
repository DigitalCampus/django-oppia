import operator
from functools import reduce

from django import forms
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse

from profile.forms import CUSTOMFIELDS_SEARCH_PREFIX
from profile.models import CustomField


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


def get_customfields_filter(value, field):
    '''
    Returns a Q object to filter a user with a custom field, taking into
    account the specific value type.
    '''
    filter_value = value
    is_list = ',' in filter_value

    if is_list:
        filter_value = filter_value.split(',')

    if field.type == 'int':
        if is_list:
            for i, elem in filter_value:
                if not isinstance(elem, int):
                    filter_value[i] = int(elem)
            filter_arg = 'userprofilecustomfield__value_int__in'
        else:
            if not isinstance(filter_value, int):
                filter_value = int(filter_value)
            filter_arg = 'userprofilecustomfield__value_int'

    elif field.type == 'bool':
        if not isinstance(filter_value, bool):
            filter_value = bool(filter_value)
        filter_arg = 'userprofilecustomfield__value_bool'

    else:
        if is_list:
            print(filter_value)
            clauses = (Q(**{'userprofilecustomfield__value_str__icontains': elem}) for elem in filter_value)
            query = reduce(operator.or_, clauses)
            query = Q(**{'userprofilecustomfield__key_name': field.id}) & query
            return query
        else:
            if not isinstance(filter_value, str):
                filter_value = str(filter_value)
            filter_arg = 'userprofilecustomfield__value_str__icontains'

    return Q(**{'userprofilecustomfield__key_name': field.id, filter_arg: filter_value})


def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search
        fields.
    '''

    query = None  # Query to search in every field
    for field_name in search_fields:
        q = Q(** {"%s__icontains" % field_name: query_string})
        query = q if query is None else (query | q)

    str_customfields = CustomField.objects.filter(type='str').order_by('order')
    for field in str_customfields:
        query = query | get_customfields_filter(query_string, field)

    return query


def get_filters_from_row(search_form, convert_date=True):
    filters = {}
    for row in search_form.cleaned_data:
        if not convert_date and (row == 'start_date' or row == 'end_date'):
            continue

        if CUSTOMFIELDS_SEARCH_PREFIX not in row \
                and search_form.cleaned_data[row]:
            if row == 'start_date':
                filters['date_joined__gte'] = search_form.cleaned_data[row]
            elif row == 'end_date':
                filters['date_joined__lte'] = search_form.cleaned_data[row]
            elif isinstance(search_form.fields[row], forms.CharField):
                filters["%s__icontains" % row] = search_form.cleaned_data[row]
            else:
                filters[row] = search_form.cleaned_data[row]
    return filters


def get_users_filtered_by_customfields(users, search_form):
    custom_fields = CustomField.objects.all().order_by('order')
    filtered = False
    for field in custom_fields:
        formfield = CUSTOMFIELDS_SEARCH_PREFIX + field.id
        if formfield in search_form.cleaned_data \
                and search_form.cleaned_data[formfield]:
            value = search_form.cleaned_data[formfield]
            print(value)
            users = users.filter(get_customfields_filter(value, field))
            filtered = True

    return users, filtered
