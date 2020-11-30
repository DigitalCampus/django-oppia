import json

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.shortcuts import render
from django.utils.decorators import method_decorator

from operator import itemgetter

from oppia.models import Tracker

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
        
@method_decorator(staff_member_required, name='dispatch')
class SearchTermView(BaseReportTemplateView):

    def process(self, request, form, start_date, end_date):
        searches = Tracker.objects.filter(type='search', 
                                          user__is_staff=False,
                                          submitted_date__gte=start_date,
                                          submitted_date__lte=end_date)
        
        search_terms = []
        
        for search in searches:
            query = self.get_query_term(search.data)
            if query is None:
                continue
            obj = {'term': query, 'count': 0}
            if obj not in search_terms:
                search_terms.append(obj)
        
        for search in searches: 
            query = self.get_query_term(search.data)
            if query is None:
                continue
            for obj in search_terms:
                if obj['term'] == query:
                    obj['count'] += 1
         
        search_terms = sorted(search_terms,
                              key=itemgetter('count'),
                              reverse=True)  
        return render(request, 'reports/search_terms.html',
                      {'form': form,
                       'search_terms': search_terms})

    def get_query_term(self, data):
        try:
            json_data = json.loads(data)
        except json.decoder.JSONDecodeError:
            return None
        if 'query' not in json_data:
            return None
        return json_data['query']
        