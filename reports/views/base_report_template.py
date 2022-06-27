from abc import abstractmethod

from collections.abc import Mapping

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from helpers.mixins.DateRangeFilterMixin import DateRangeFilterMixin
from reports import constants
from summary.models import UserCourseSummary


@method_decorator(staff_member_required, name='dispatch')
class BaseReportTemplateView(DateRangeFilterMixin, TemplateView):

    users_filter_by = None
    daterange_no_days = constants.ANNUAL_NO_DAYS

    def dispatch(self, request, *args, **kwargs):
        self.users_filter_by = UserCourseSummary.get_excluded_users()
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date, end_date = self.get_daterange()
        data = self.get_graph_data(start_date, end_date)
        if isinstance(data, Mapping):
            context.update(data)
        else:
            context['activity_graph_data'] = data
        return context

    @abstractmethod
    def get_graph_data(self, start_date, end_date):
        pass
