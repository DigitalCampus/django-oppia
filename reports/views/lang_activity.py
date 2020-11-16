
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from oppia.models import Tracker, Course

from reports.views.base_report_template import BaseReportTemplateView


@method_decorator(staff_member_required, name='dispatch')
class LanguageActivityView(BaseReportTemplateView):

    def process(self, request, form, start_date):
        hit_by_language = Tracker.objects \
            .filter(user__is_staff=False) \
            .exclude(lang=None) \
            .values('lang') \
            .annotate(total_hits=Count('id')) \
            .order_by('-total_hits')
        total_hits = Tracker.objects \
            .filter(user__is_staff=False) \
            .exclude(lang=None) \
            .aggregate(total_hits=Count('id'))

        i = 0
        languages = []
        other_languages = 0
        for hbl in hit_by_language:
            if i < 10:
                hits_percent = float(hbl['total_hits']
                                     * 100.0
                                     / total_hits['total_hits'])
                languages.append({'lang': hbl['lang'],
                                  'hits_percent': hits_percent})
            else:
                other_languages += hbl['total_hits']
            i += 1
        if i > 10:
            hits_percent = float(other_languages
                                 * 100.0
                                 / total_hits['total_hits'])
            languages.append({'lang': _('Other'),
                              'hits_percent': hits_percent})
        return render(request, 'reports/lang_activity.html',
                      {'form': form,
                       'languages': languages})
