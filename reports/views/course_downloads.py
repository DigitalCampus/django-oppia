
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.shortcuts import render
from django.utils.decorators import method_decorator

from reports.views.base_report_template import BaseReportTemplateView

from summary.models import CourseDailyStats


@method_decorator(staff_member_required, name='dispatch')
class CourseDownloadsView(BaseReportTemplateView):

    def process(self, request, form, start_date):
        course_downloads = CourseDailyStats.objects \
            .filter(day__gte=start_date, type='download') \
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

        return render(request, 'reports/course_downloads.html',
                      {'form': form,
                       'course_downloads': course_downloads,
                       'previous_course_downloads':
                       previous_course_downloads})
