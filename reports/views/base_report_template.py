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
        start_date = datetime.date.today() - datetime.timedelta(
            days=constants.ANNUAL_NO_DAYS)
        end_date = datetime.date.today()
        data = {}
        data['start_date'] = start_date.strftime(dates.DATE_FORMAT)
        data['end_date'] = end_date.strftime(dates.DATE_FORMAT)
        form = dates.DateRangeForm(initial=data)

        return self.process(request, form, start_date, end_date)

    def post(self, request):
        dashboard_accessed.send(sender=None, request=request, data=None)
        start_date = datetime.date.today() - datetime.timedelta(
            days=constants.ANNUAL_NO_DAYS)
        end_date = datetime.date.today()
        form = dates.DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
        
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        return self.process(request, form, start_date, end_date)

    @abstractmethod
    def process(self, request, form, start_date, end_date):
        pass
