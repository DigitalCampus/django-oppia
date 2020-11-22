
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from reports.views.base_report_template import BaseReportTemplateView

from viz.models import UserLocationVisualization


@method_decorator(staff_member_required, name='dispatch')
class CountriesView(BaseReportTemplateView):

    def process(self, request, form, start_date):
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
                hits_percent = float(c['country_total_hits']
                                     * 100.0
                                     / total_hits['total_hits'])
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
        return render(request, 'reports/countries.html',
                      {'form': form,
                       'total_countries': total_countries,
                       'country_activity': country_activity})
