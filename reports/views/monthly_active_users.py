import datetime

from dateutil.relativedelta import relativedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from profile.models import UserProfileCustomField

from oppia import constants as oppia_constants
from reports import constants as reports_constants
from summary.models import DailyActiveUsers, DailyActiveUser
from reports.forms import ReportGroupByForm


@method_decorator(staff_member_required, name='dispatch')
class MonthlyActiveUsersView(TemplateView):

    def get(self, request):
        start_date = timezone.now() - relativedelta(months=reports_constants.MAUS_DEFAULT_NO_MONTHS)
        end_date = timezone.now()
        
        delta = relativedelta(months=+1)

        no_months = 0
        tmp_date = start_date
        while tmp_date <= end_date:
            tmp_date += delta
            no_months += 1
        
        data = []
        for i in range(0, no_months, +1):
            temp = start_date + relativedelta(months=+i)
            month = temp.strftime("%m")
            year = temp.strftime("%Y")
            try:
                summary_count_no_admin = DailyActiveUser.objects \
                    .filter(dau__day__month=month,
                            dau__day__year=year,
                            user__is_staff=False) \
                    .aggregate(total_submitted_date=Count('user'))
                data.append([temp.strftime(oppia_constants.STR_DATE_FORMAT_MONTH),
                             0,
                             summary_count_no_admin['total_submitted_date']])
            except DailyActiveUser.DoesNotExist:
                data.append(
                    [temp.strftime(oppia_constants.STR_DATE_FORMAT_MONTH), 0, 0])

        group_by_form = ReportGroupByForm()
        return render(request, 'reports/maus.html',
                      {'data': data,
                       'form': group_by_form})
