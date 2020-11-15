
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear
from django.shortcuts import render
from django.utils.decorators import method_decorator

from reports.views.base_report_template import BaseReportTemplateView


@method_decorator(staff_member_required, name='dispatch')
class UserRegistrationsView(BaseReportTemplateView):

    def process(self, request, form, start_date):
        user_registrations = User.objects.filter(
            date_joined__gte=start_date,
            is_staff=False) \
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
