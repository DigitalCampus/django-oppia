from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear

from reports.views.base_report_template import BaseReportTemplateView


class UserRegistrationsView(BaseReportTemplateView):

    template_name = 'reports/user_registrations.html'

    def get_graph_data(self, start_date, end_date):

        user_registrations = User.objects\
            .filter(date_joined__gte=start_date, date_joined__lte=end_date) \
            .exclude(pk__in=self.users_filter_by) \
            .annotate(month=TruncMonth('date_joined'),
                      year=TruncYear('date_joined')) \
            .values('month', 'year') \
            .annotate(count=Count('id')) \
            .order_by('year', 'month')

        previous_user_registrations = User.objects.filter(date_joined__lt=start_date).count()

        return {
            'user_registrations': user_registrations,
            'previous_user_registrations': previous_user_registrations
        }
