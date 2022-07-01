import datetime

from reports.views.base_report_template import BaseReportTemplateView
from settings import constants
from settings.models import SettingProperties
from summary.models import UserCourseDailySummary


class InactiveUsersView(BaseReportTemplateView):

    template_name = 'reports/inactive_users.html'

    def get_graph_data(self, start_date, end_date):

        data = {}
        total_users = UserCourseDailySummary.objects\
            .exclude(user__in=self.users_filter_by)\
            .values('user').distinct().count()

        if total_users == 0:
            return {}

        data['total_users'] = total_users

        active_last_month = self.users_active_since(end_date - datetime.timedelta(days=31))
        data['inactive_one_month_no'] = total_users - active_last_month
        data['inactive_one_month_percent'] = int((total_users - active_last_month) * 100 / total_users)

        active_three_month = self.users_active_since(end_date - datetime.timedelta(days=91))
        data['inactive_three_month_no'] = total_users - active_three_month
        data['inactive_three_month_percent'] = int((total_users - active_three_month) * 100 / total_users)

        active_six_month = self.users_active_since(end_date - datetime.timedelta(days=183))
        data['inactive_six_month_no'] = total_users - active_six_month
        data['inactive_six_month_percent'] = int((total_users - active_six_month) * 100 / total_users)

        data['years'] = []
        for i in range(1, SettingProperties.get_property(
                constants.OPPIA_DATA_RETENTION_YEARS, 999) + 1):
            days = i * 365
            year_date = end_date - datetime.timedelta(days=days)
            active_years = self.users_active_since(year_date)
            year_data = {}
            year_data['year'] = i
            year_data['inactive_no'] = total_users - active_years
            year_data['inactive_percent'] = int((total_users - active_years) * 100 / total_users)
            data['years'].append(year_data)

        return {'inactive_user_data': data}

    def users_active_since(self, day):
        return UserCourseDailySummary.objects \
            .filter(day__gte=day) \
            .exclude(user__in=self.users_filter_by) \
            .values("user").distinct().count()
