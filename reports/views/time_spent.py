import datetime
from collections import OrderedDict

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils.decorators import method_decorator

from oppia import constants as oppia_constants

from reports.views.base_report_template import BaseReportTemplateView

from summary.models import DailyActiveUsers


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
            parts.append('{} {}{}'.format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)

@method_decorator(staff_member_required, name='dispatch')
class AverageTimeSpentView(BaseReportTemplateView):

    def process(self, request, form, start_date, end_date):
        data = []
        max_time = 0
        no_days = (end_date - start_date).days + 1
        for i in range(0, no_days, +1):
            temp = start_date + datetime.timedelta(days=i)
            try:
                avg_time = DailyActiveUsers.objects.get(
                    day=temp.strftime(oppia_constants.STR_DATE_FORMAT))
                time_spent = avg_time.get_avg_time_spent()
                if time_spent > max_time:
                    max_time = time_spent
                data.append([temp.strftime(
                    oppia_constants.STR_DATE_DISPLAY_FORMAT),
                    int(round(time_spent)),
                    seconds_to_hours(int(round(time_spent)))])
            except DailyActiveUsers.DoesNotExist:
                data.append(
                    [temp.strftime(oppia_constants.STR_DATE_DISPLAY_FORMAT),
                     0, 0])

        return render(request, 'reports/average_time_spent.html',
                      {'activity_graph_data': data,
                       'form': form,
                       'max_time': max_time })



@method_decorator(staff_member_required, name='dispatch')
class TotalTimeSpentView(BaseReportTemplateView):

    def process(self, request, form, start_date, end_date):
        data = []
        max_time = 0
        no_days = (end_date - start_date).days + 1
        for i in range(0, no_days, +1):
            temp = start_date + datetime.timedelta(days=i)
            try:
                summary_count_time_total = DailyActiveUsers.objects.get(
                    day=temp.strftime(oppia_constants.STR_DATE_FORMAT))
                time_spent = summary_count_time_total.get_total_time_spent()
                if time_spent > max_time:
                    max_time = time_spent
                data.append([temp.strftime(
                    oppia_constants.STR_DATE_DISPLAY_FORMAT), 
                    int(round(time_spent)),
                    seconds_to_hours(int(round(time_spent)))])
            except DailyActiveUsers.DoesNotExist:
                data.append(
                    [temp.strftime(oppia_constants.STR_DATE_DISPLAY_FORMAT),
                     0, 0])
        return render(request, 'reports/total_time_spent.html',
                      {'activity_graph_data': data,
                       'form': form,
                       'max_time': max_time })
