import json
from operator import itemgetter

from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear

from oppia.models import Tracker
from reports.views.base_report_template import BaseReportTemplateView
from summary.models import CourseDailyStats


class SearchesView(BaseReportTemplateView):

    template_name = 'reports/searches.html'

    def get_graph_data(self, start_date, end_date):
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

        return {
            'searches': searches,
            'previous_searches': previous_searches
        }


class SearchTermView(BaseReportTemplateView):

    template_name = 'reports/search_terms.html'

    def get_graph_data(self, start_date, end_date):
        searches = Tracker.objects.filter(type='search', user__is_staff=False,
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

        return {'search_terms': search_terms}

    def get_query_term(self, data):
        try:
            json_data = json.loads(data)
        except json.decoder.JSONDecodeError:
            return None
        if 'query' not in json_data:
            return None
        return json_data['query']
