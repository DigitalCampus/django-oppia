from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear

from reports.views.base_report_template import BaseReportTemplateView
from summary.models import CourseDailyStats


class CourseDownloadsView(BaseReportTemplateView):

    template_name = 'reports/course_downloads.html'

    def get_graph_data(self, start_date, end_date):

        daily_downloads = CourseDailyStats.objects \
            .filter(day__gte=start_date,  day__lte=end_date,  type='download') \
            .values('day') \
            .annotate(count=Sum('total')) \
            .order_by('day')

        course_downloads = CourseDailyStats.objects \
            .filter(day__gte=start_date, day__lte=end_date, type='download') \
            .annotate(month=TruncMonth('day'),
                      year=TruncYear('day')) \
            .values('month', 'year') \
            .annotate(count=Sum('total')) \
            .order_by('year', 'month')

        previous_course_downloads = CourseDailyStats.objects \
            .filter(day__lt=start_date, type='download') \
            .aggregate(total=Sum('total')) \
            .get('total', 0)
        if previous_course_downloads is None:
            previous_course_downloads = 0

        return {
            'daily_downloads': daily_downloads,
            'course_downloads': course_downloads,
            'previous_course_downloads':previous_course_downloads
        }
