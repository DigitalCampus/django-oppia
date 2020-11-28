import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from oppia import constants as oppia_constants

from reports import constants as reports_constants
from reports.forms import ReportGroupByForm
from reports.signals import dashboard_accessed
from reports.views.base_report_template import BaseReportTemplateView

from summary.models import DailyActiveUsers


@method_decorator(staff_member_required, name='dispatch')
class AverageTimeSpentView(BaseReportTemplateView):

    def process(self, request, form, start_date, end_date):
        data = []
        no_days = (end_date - start_date).days + 1
        for i in range(0, no_days, +1):
            temp = start_date + datetime.timedelta(days=i)
            try:
                avg_time = DailyActiveUsers.objects.get(
                    day=temp.strftime("%Y-%m-%d"))
                time_spent = avg_time.get_avg_time_spent()
                data.append([temp.strftime(
                    oppia_constants.STR_DATE_FORMAT),
                    time_spent])
            except DailyActiveUsers.DoesNotExist:
                data.append(
                    [temp.strftime(oppia_constants.STR_DATE_FORMAT), 0])

        return render(request, 'reports/average_time_spent.html',
                      {'activity_graph_data': data,
                       'form': form})


@method_decorator(staff_member_required, name='dispatch')
class TotalTimeSpentView(BaseReportTemplateView):

    def process(self, request, form, start_date, end_date):
        data = []
        no_days = (end_date - start_date).days + 1
        for i in range(0, no_days, +1):
            temp = start_date + datetime.timedelta(days=i)
            try:
                summary_count_time_total = DailyActiveUsers.objects.get(
                    day=temp.strftime("%Y-%m-%d"))
                time_spent = summary_count_time_total.get_total_time_spent()
                data.append([temp.strftime(oppia_constants.STR_DATE_FORMAT),
                             time_spent])
            except DailyActiveUsers.DoesNotExist:
                data.append(
                    [temp.strftime(oppia_constants.STR_DATE_FORMAT), 0])
        return render(request, 'reports/total_time_spent.html',
                      {'activity_graph_data': data,
                       'form': form})
