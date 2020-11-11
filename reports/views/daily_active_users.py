import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count
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
class DailyActiveUsersView(TemplateView):

    def get(self, request):
        start_date = timezone.now() - datetime.timedelta(
            days=reports_constants.DAUS_DEFAULT_NO_DAYS)
        end_date = timezone.now()
        data = []
        no_days = (end_date - start_date).days + 1
        for i in range(0, no_days, +1):
            temp = start_date + datetime.timedelta(days=i)
            try:
                summary_counts_no_admin = DailyActiveUser.objects.filter(
                    dau__day=temp.strftime("%Y-%m-%d"),
                    user__is_staff=False) \
                    .aggregate(total_submitted_date=Count('user'))
                data.append([temp.strftime(oppia_constants.STR_DATE_FORMAT),
                             0,
                             summary_counts_no_admin['total_submitted_date']])
            except DailyActiveUsers.DoesNotExist:
                data.append(
                    [temp.strftime(oppia_constants.STR_DATE_FORMAT), 0, 0])

        group_by_form = ReportGroupByForm()
        return render(request, 'reports/daus.html',
                      {'data': data,
                       'form': group_by_form})
