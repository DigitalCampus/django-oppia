from django.core.paginator import Paginator

from oppia.models import Course


def get_paginated_courses(request):
    default_order = 'lastupdated_date'
    ordering = request.GET.get('order_by', None)
    if ordering is None:
        ordering = default_order

    courses = Course.objects.all().order_by(ordering)
    paginator = Paginator(courses, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    return ordering, paginator.page(page)


def generate_graph_data(dates_types_stats, is_monthly=False):
    dates = []

    current_date = None
    current_stats = {}

    for date in dates_types_stats:
        if is_monthly:
            # depending if it is monthly or daily, we parse differently the
            # day "tag"
            day = date['month']
        else:
            day = date['stat_date']

        if current_date is None or day != current_date:
            if current_date is not None:
                dates.append([current_date, current_stats])
            current_date = day
            current_stats = {'page': 0,
                             'quiz': 0,
                             'media': 0,
                             'resource': 0,
                             'total': 0}

        current_stats[date['type']] = date['total']
        current_stats['total'] += date['total']

    if current_date is not None:
        dates.append([current_date, current_stats])

    return dates
