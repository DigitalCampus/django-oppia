import datetime

from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth, TruncYear

from oppia import constants
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


def filter_trackers(trackers, start_date, end_date):

    activity = []
    no_days = (end_date - start_date).days + 1

    trackers = trackers.filter(
                        tracker_date__gte=start_date,
                        tracker_date__lte=end_date) \
                       .annotate(day=TruncDay('tracker_date'),
                                 month=TruncMonth('tracker_date'),
                                 year=TruncYear('tracker_date')) \
                       .values('day') \
                       .annotate(count=Count('id'))
    for i in range(0, no_days, +1):
        temp = start_date + datetime.timedelta(days=i)
        temp_date = temp.date().strftime(constants.STR_DATE_DISPLAY_FORMAT)
        count = next((dct['count']
                     for dct in trackers
                     if dct['day'].strftime(constants.STR_DATE_DISPLAY_FORMAT)
                     == temp_date), 0)
        activity.append([temp_date, count])

    return activity
