import datetime

from abc import abstractmethod

from django.utils import timezone
from django.views.generic import TemplateView

from helpers.forms import dates

from reports import constants
from reports.signals import dashboard_accessed


class BaseReportTemplateView(TemplateView):

    def get(self, request):
        dashboard_accessed.send(sender=None, request=request, data=None)
        start_date = timezone.now() - datetime.timedelta(
            days=constants.ANNUAL_NO_DAYS)
        data = {}
        data['start_date'] = start_date.strftime(dates.DATE_FORMAT)
        form = dates.DateDiffForm(initial=data)

        return self.process(request, form, start_date)

    def post(self, request):
        dashboard_accessed.send(sender=None, request=request, data=None)
        start_date = timezone.now() - datetime.timedelta(
            days=constants.ANNUAL_NO_DAYS)
        form = dates.DateDiffForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get("start_date")

        return self.process(request, form, start_date)

    @abstractmethod
    def process(self, request, form, start_date):
        pass
