
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.shortcuts import render
from django.utils.decorators import method_decorator

from reports.views.base_report_template import BaseReportTemplateView

from summary.models import CourseDailyStats


@method_decorator(staff_member_required, name='dispatch')
class SearchesView(BaseReportTemplateView):

    def process(self, request, form, start_date, end_date):
        searches = CourseDailyStats.objects \
            .filter(day__gte=start_date,
                    day__lte=end_date,
                    type='search') \
            .annotate(month=TruncMonth('day'),
                      year=TruncYear('day')) \
            .values('month', 'year') \
            .annotate(count=Sum('total')) \
            .order_by('year', 'month')

        previous_searches = CourseDailyStats.objects \
            .filter(day__lt=start_date,
                    type='search') \
            .aggregate(total=Sum('total')) \
            .get('total', 0)
        if previous_searches is None:
            previous_searches = 0
        return render(request, 'reports/searches.html',
                      {'form': form,
                       'searches': searches,
                       'previous_searches':
                       previous_searches})
