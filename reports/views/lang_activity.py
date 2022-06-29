from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from oppia.models import Tracker
from reports.views.base_report_template import BaseReportTemplateView


class LanguageActivityView(BaseReportTemplateView):
    template_name = 'reports/lang_activity.html'

    def get_graph_data(self, start_date, end_date):
        hit_by_language = Tracker.objects \
            .filter(user__is_staff=False, submitted_date__gte=start_date, submitted_date__lte=end_date) \
            .exclude(lang=None) \
            .values('lang') \
            .annotate(total_hits=Count('id')) \
            .order_by('-total_hits')
        total_hits = Tracker.objects \
            .filter(user__is_staff=False, submitted_date__gte=start_date, submitted_date__lte=end_date) \
            .exclude(lang=None) \
            .aggregate(total_hits=Count('id'))

        i = 0
        languages = []
        other_languages = 0
        for hbl in hit_by_language:
            if i < 10:
                hits_percent = float(hbl['total_hits'] * 100.0 / total_hits['total_hits'])
                languages.append({'lang': hbl['lang'], 'hits_percent': hits_percent})
            else:
                other_languages += hbl['total_hits']
            i += 1
        if i > 10:
            hits_percent = float(other_languages
                                 * 100.0
                                 / total_hits['total_hits'])
            languages.append({'lang': _('Other'),
                              'hits_percent': hits_percent})

        return {'languages': languages }