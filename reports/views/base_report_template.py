import datetime

from abc import abstractmethod

from django.utils import timezone
from django.views.generic import TemplateView

from helpers.forms import dates

from oppia import constants as oppia_constants
from reports import constants
from reports.signals import dashboard_accessed


class BaseReportTemplateView(TemplateView):

    def get(self, request):
        
        start_date = datetime.date.today() - datetime.timedelta(
            days=constants.ANNUAL_NO_DAYS)
        end_date = datetime.date.today()
        data = {}
        data['start_date'] = start_date.strftime(
            oppia_constants.STR_DATE_FORMAT)
        data['end_date'] = end_date.strftime(
            oppia_constants.STR_DATE_FORMAT)
        form = dates.DateRangeForm(initial=data)
        dashboard_accessed.send(sender=None, request=request, data=data)

        return self.process(request, form, start_date, end_date)

    def post(self, request):
        start_date = datetime.date.today() - datetime.timedelta(
            days=constants.ANNUAL_NO_DAYS)
        end_date = datetime.date.today()
        form = dates.DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
        
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(
                start_date,
                oppia_constants.STR_DATE_FORMAT)
        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(
                end_date,
                oppia_constants.STR_DATE_FORMAT)
        data = {}
        data['start_date'] = start_date
        data['end_date'] = end_date
        dashboard_accessed.send(sender=None, request=request, data=data)
        return self.process(request, form, start_date, end_date)

    @abstractmethod
    def process(self, request, form, start_date, end_date):
        pass
