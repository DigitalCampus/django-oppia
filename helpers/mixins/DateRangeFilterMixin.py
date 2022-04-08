import datetime

from django.utils import timezone

from helpers.forms.dates import DateRangeForm
from oppia.constants import ACTIVITY_GRAPH_DEFAULT_NO_DAYS, STR_DATE_FORMAT


class DateRangeFilterMixin(object):
    """
    A mixin to add the common functionality when a view has a date-rangefilter
    """
    daterange_form_class = DateRangeForm
    daterange_form_method = 'get'
    daterange_form_context_name = 'form'
    daterange_form_initial = {}

    def __init__(self):
        self.daterange_form_instance = None

    # Gets the default daterange from today back to the one month
    def get_initial_daterange(self):
        start_date = timezone.now() - datetime.timedelta(days=ACTIVITY_GRAPH_DEFAULT_NO_DAYS)
        end_date = timezone.now()

        return {
            'start_date': start_date.strftime(STR_DATE_FORMAT),
            'end_date': end_date.strftime(STR_DATE_FORMAT)
        }

    def get_daterange_form(self):
        if not self.daterange_form_instance:
            initial = self.daterange_form_initial.copy()
            initial.update(self.get_initial_daterange())
            initial.update(self.request.GET.dict())
            self.daterange_form_instance = self.daterange_form_class(initial)
            self.daterange_form_instance.form_method = self.daterange_form_method

        return self.daterange_form_instance

    def get_daterange(self):
        form = self.get_daterange_form()
        if form.is_valid():
            current_tz = timezone.get_current_timezone()
            start_date = timezone.make_aware(
                datetime.datetime.strptime(form.cleaned_data.get("start_date"), STR_DATE_FORMAT), current_tz)
            end_date = timezone.make_aware(
                datetime.datetime.strptime(form.cleaned_data.get("end_date"), STR_DATE_FORMAT), current_tz)

            return start_date, end_date
        else:
            dates = self.get_initial_daterange()
            return dates['start_date'], dates['end_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.daterange_form_context_name] = self.get_daterange_form()

        return context
