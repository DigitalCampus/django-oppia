# viz/views.py
import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from helpers.forms.dates import DateDiffForm
from oppia.models import Tracker, Course
from summary.models import CourseDailyStats
from viz.models import UserLocationVisualization

from settings import constants
from settings.models import SettingProperties


@method_decorator(staff_member_required, name='dispatch')
class Summary(TemplateView):

    STR_YEAR_DAY = "year(day)"
    STR_MONTH_DAY = "month(day)"

    def get(self, request):
        start_date = timezone.now() - datetime.timedelta(days=365)
        data = {}
        data['start_date'] = start_date.strftime("%Y-%m-%d")
        form = DateDiffForm(initial=data)
        return self.process_response(request, form, start_date)

    def post(self, request):
        start_date = timezone.now() - datetime.timedelta(days=365)
        form = DateDiffForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get("start_date")
        return self.process_response(request, form, start_date)

    def process_response(self, request, form, start_date):

        # Countries
        total_countries, country_activity = self.get_countries(start_date)


        return render(request, 'viz/summary.html',
                      {'form': form,
                       'total_countries': total_countries,
                       'country_activity': country_activity})

    def get_countries(self, start_date):
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

        return total_countries, country_activity
