import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from helpers.forms.dates import DateDiffForm
from oppia.models import Tracker, Course

from helpers.forms import dates

@method_decorator(staff_member_required, name='dispatch')
class UserRegistrationsView(TemplateView):
    
    def get(self, request):
        start_date = timezone.now() - datetime.timedelta(days=365)
        data = {}
        data['start_date'] = start_date.strftime(dates.DATE_FORMAT)
        form = DateDiffForm(initial=data)

        return self.process(request, form, start_date)

    def post(self, request):
        start_date = timezone.now() - datetime.timedelta(days=365)
        form = DateDiffForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get("start_date")

        return self.process(request, form, start_date)

    def process(self, request, form, start_date):
        user_registrations = User.objects.filter(date_joined__gte=start_date) \
            .annotate(month=TruncMonth('date_joined'),
                      year=TruncYear('date_joined')) \
            .values('month', 'year') \
            .annotate(count=Count('id')) \
            .order_by('year', 'month')
        previous_user_registrations = User.objects \
            .filter(date_joined__lt=start_date).count()
        return render(request, 'reports/user_registrations.html',
                      {'form': form,
                       'user_registrations': user_registrations,
                       'previous_user_registrations':
                       previous_user_registrations})
