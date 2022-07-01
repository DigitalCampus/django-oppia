import datetime

from dateutil.relativedelta import relativedelta

from oppia import constants as oppia_constants

from reports.views.base_report_template import BaseReportTemplateView
from summary.models import UserCourseDailySummary


class DailyActiveUsersView(BaseReportTemplateView):
    template_name = 'reports/daus.html'

    def get_graph_data(self, start_date, end_date):
        data = []
        no_days = (end_date - start_date).days + 1
        for i in range(0, no_days, +1):
            day = start_date + datetime.timedelta(days=i)

            num_users = UserCourseDailySummary.objects.filter(
                day=day).exclude(user__in=self.users_filter_by).values('user').distinct().count()

            data.append([day.strftime(oppia_constants.STR_DATE_DISPLAY_FORMAT), num_users])

        return data


class MonthlyActiveUsersView(BaseReportTemplateView):

    template_name = 'reports/maus.html'

    def get_graph_data(self, start_date, end_date):
        delta = relativedelta(months=+1)
        no_months = 0
        tmp_date = start_date
        while tmp_date <= end_date:
            tmp_date += delta
            no_months += 1

        data = []
        for i in range(0, no_months, +1):
            date = start_date + relativedelta(months=+i)
            num_users = UserCourseDailySummary.objects.filter(
                day__month=date.month,
                day__year=date.year).exclude(user__in=self.users_filter_by).values('user').distinct().count()

            data.append([date.strftime(oppia_constants.STR_DATE_DISPLAY_FORMAT_MONTH), num_users])

        return data
