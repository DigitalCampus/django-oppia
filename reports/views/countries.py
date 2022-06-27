from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from reports.views.base_report_template import BaseReportTemplateView
from viz.models import UserLocationVisualization


class CountriesView(BaseReportTemplateView):

    template_name = 'reports/countries.html'

    def get_graph_data(self, start_date, end_date):
        hits_by_country = UserLocationVisualization.objects.all() \
            .values('country_code',
                    'country_name') \
            .annotate(country_total_hits=Sum('hits')) \
            .order_by('-country_total_hits')
        total_hits = UserLocationVisualization.objects.all() \
            .aggregate(total_hits=Sum('hits'))
        total_countries = hits_by_country.count()

        i = 0
        country_activity = []
        other_country_activity = 0
        for c in hits_by_country:
            if i < 20:
                hits_percent = float(c['country_total_hits'] * 100.0 / total_hits['total_hits'])
                country_activity.append({'country_code': c['country_code'],
                                         'country_name': c['country_name'],
                                         'hits_percent': hits_percent})
            else:
                other_country_activity += c['country_total_hits']
            i += 1
        if i > 20:
            hits_percent = float(other_country_activity
                                 * 100.0
                                 / total_hits['total_hits'])
            country_activity.append({'country_code': None,
                                     'country_name': _('Other'),
                                     'hits_percent': hits_percent})
        return {
               'total_countries': total_countries,
               'country_activity': country_activity
        }
