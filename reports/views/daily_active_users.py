import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from profile.models import UserProfileCustomField

from oppia import constants
from oppia.models import Tracker
from reports.forms import ReportGroupByForm


@method_decorator(staff_member_required, name='dispatch')
class DailyActiveUsers(TemplateView):

    def get(self, request):
        start_date = timezone.now() - datetime.timedelta(
            days=constants.ACTIVITY_GRAPH_DEFAULT_NO_DAYS)
        end_date = timezone.now()
        data = []
        no_days = (end_date - start_date).days + 1
        recent_trackers = Tracker.objects.filter(submitted_date__gte=start_date)
        for i in range(0, no_days, +1):
            temp = start_date + datetime.timedelta(days=i)
            day = temp.strftime("%d")
            month = temp.strftime("%m")
            year = temp.strftime("%Y")
            count = recent_trackers.filter(submitted_date__day=day,
                                           submitted_date__month=month,
                                           submitted_date__year=year).values('user').distinct().count()
            data.append([temp.strftime(constants.STR_DATE_FORMAT), count])

        group_by_form = ReportGroupByForm()
        return render(request, 'reports/daus.html',
                      {'data': data,
                       'form': group_by_form})
