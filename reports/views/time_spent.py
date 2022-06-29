import datetime

from django.db.models import Avg, Sum

from oppia import constants as oppia_constants
from reports.views.base_report_template import BaseReportTemplateView
from summary.models import UserCourseDailySummary


def seconds_to_hours(seconds):
    TIME_DURATION_UNITS = (
            ('week', 60*60*24*7),
            ('day', 60*60*24),
            ('hour', 60*60),
            ('min', 60),
            ('sec', 1)
            )
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


class AverageTimeSpentView(BaseReportTemplateView):

    template_name = 'reports/average_time_spent.html'

    def get_graph_data(self, start_date, end_date):
        data = []
        max_time = 0
        no_days = (end_date - start_date).days + 1
        for i in range(0, no_days, +1):
            day = start_date + datetime.timedelta(days=i)
            time_spent = UserCourseDailySummary.objects.filter(day=day).aggregate(avg=Avg('time_spent_tracked'))['avg']
            if time_spent is None:
                time_spent = 0
            max_time = max(max_time, time_spent)
            data.append([
                day.strftime(oppia_constants.STR_DATE_DISPLAY_FORMAT),
                int(round(time_spent)),
                seconds_to_hours(int(round(time_spent)))]
            )

        return {
            'activity_graph_data': data,
            'max_time': max_time
        }


class TotalTimeSpentView(BaseReportTemplateView):

    template_name = 'reports/total_time_spent.html'

    def get_graph_data(self, start_date, end_date):
        data = []
        max_time = 0
        no_days = (end_date - start_date).days + 1

        for i in range(0, no_days, +1):
            day = start_date + datetime.timedelta(days=i)
            time_spent = UserCourseDailySummary.objects.filter(day=day).aggregate(sum=Sum('time_spent_tracked'))['sum']
            if time_spent is None:
                time_spent = 0
            max_time = max(max_time, time_spent)
            data.append([
                day.strftime(oppia_constants.STR_DATE_DISPLAY_FORMAT),
                int(round(time_spent)),
                seconds_to_hours(int(round(time_spent)))]
            )

        return {
            'activity_graph_data': data,
            'max_time': max_time
        }