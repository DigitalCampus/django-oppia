import datetime
import tablib

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator

from oppia import constants as oppia_constants

from reports.views.base_report_template import BaseReportTemplateView

from summary.models import DailyActiveUser


@method_decorator(staff_member_required, name='dispatch')
class DownloadTimeSpentView(BaseReportTemplateView):
    
    def process(self, request, form, start_date, end_date):
        
        headers = ('date',
                   'user_id',
                   'username',
                   'course',
                   'course_title',
                   'time_spent')
        data = []
        data = tablib.Dataset(*data, headers=headers)
        
        # get all the users who have some time spent in a day
        active_users_days = DailyActiveUser.objects.filter(
            type=DailyActiveUser.TRACKER)
        
        for aud in active_users_days:
            data.append(
                        (
                           aud.dau.day,
                           aud.user.id,
                           aud.user.username,
                           aud.course.shortname,
                           aud.course.get_title(),
                           aud.time_spent
                        )
                    )
            
        response = HttpResponse(data.csv,
                                content_type='application/text;charset=utf-8')
        response['Content-Disposition'] = \
            "attachment; filename=time_tracking.csv"

        return response
        
        