import datetime

from dateutil.relativedelta import relativedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render
from django.utils.decorators import method_decorator

from reports import constants as reports_constants
from reports.views.base_report_template import BaseReportTemplateView

from settings import constants
from settings.models import SettingProperties

from summary.models import DailyActiveUser


@method_decorator(staff_member_required, name='dispatch')
class InactiveUsersView(BaseReportTemplateView):
    
    def process(self, request, form, start_date, end_date):
        data = {}

        total_users = DailyActiveUser.objects.filter(
                user__is_staff=False,
                user__is_superuser=False).values("user").distinct().count()

        if total_users == 0:
            return render(request, 'reports/inactive_users.html',
                      {'form': form})
               
        data['total_users'] = total_users
        

        one_month_date = end_date - datetime.timedelta(days=31)
        active_one_month = DailyActiveUser.objects.filter(
            user__is_staff=False,
            user__is_superuser=False,
            dau__day__gte=one_month_date).values("user").distinct().count()
        data['inactive_one_month_no'] = total_users - active_one_month
        data['inactive_one_month_percent'] = \
            int((total_users - active_one_month) * 100 / total_users)
        
        three_month_date = end_date - datetime.timedelta(days=91)
        active_three_month = DailyActiveUser.objects.filter(
            user__is_staff=False,
            user__is_superuser=False,
            dau__day__gte=three_month_date).values("user").distinct().count()
        data['inactive_three_month_no'] = total_users - active_three_month
        data['inactive_three_month_percent'] =  \
            int((total_users - active_three_month) * 100 / total_users)

        six_month_date = end_date - datetime.timedelta(days=183)
        active_six_month = DailyActiveUser.objects.filter(
            user__is_staff=False,
            user__is_superuser=False,
            dau__day__gte=six_month_date).values("user").distinct().count()
        data['inactive_six_month_no'] = total_users - active_six_month
        data['inactive_six_month_percent'] = \
            int((total_users - active_six_month) * 100 / total_users)

        data['years'] = []
        for i in range(1, SettingProperties.get_property(
            constants.OPPIA_DATA_RETENTION_YEARS, 999) + 1):
            days = i * 365
            year_date = end_date - datetime.timedelta(days=days)
            active_years = DailyActiveUser.objects.filter(
                user__is_staff=False,
                user__is_superuser=False,
                dau__day__gte=year_date).values("user").distinct().count()
            year_data = {}
            year_data['year'] = i
            year_data['inactive_no'] = total_users - active_years
            year_data['inactive_percent']= \
                int((total_users - active_years) * 100 / total_users)
            data['years'].append(year_data)

        return render(request, 'reports/inactive_users.html',
                      {'inactive_user_data': data,
                       'form': form})
