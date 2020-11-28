import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _

from oppia.models import Course

from reports.views.base_report_template import BaseReportTemplateView

from summary.models import CourseDailyStats


@method_decorator(staff_member_required, name='dispatch')
class CourseActivityView(BaseReportTemplateView):

    def process(self, request, form, start_date, end_date):
        course_activity = CourseDailyStats.objects \
            .filter(day__gte=start_date,
                    day__lte=end_date) \
            .annotate(month=TruncMonth('day'),
                      year=TruncYear('day')) \
            .values('month', 'year') \
            .annotate(count=Sum('total')) \
            .order_by('year', 'month')

        previous_course_activity = CourseDailyStats.objects \
            .filter(day__lt=start_date) \
            .aggregate(total=Sum('total')) \
            .get('total', 0)
        if previous_course_activity is None:
            previous_course_activity = 0

        last_month = timezone.now() - datetime.timedelta(days=131)

        hit_by_course = CourseDailyStats.objects \
            .filter(day__gte=last_month, course__isnull=False) \
            .values('course_id') \
            .annotate(total_hits=Sum('total')) \
            .order_by('-total_hits')
        total_hits = sum(cstats['total_hits'] for cstats in hit_by_course)

        i = 0
        hot_courses = []
        other_course_activity = 0
        for hbc in hit_by_course:
            if i < 10:
                hits_percent = float(hbc['total_hits'] * 100.0 / total_hits)
                course = Course.objects.get(id=hbc['course_id'])
                hot_courses.append({'course': course,
                                    'hits_percent': hits_percent})
            else:
                other_course_activity += hbc['total_hits']
            i += 1
        if i > 10:
            hits_percent = float(other_course_activity * 100.0 / total_hits)
            hot_courses.append({'course': _('Other'),
                                'hits_percent': hits_percent})
        return render(request, 'reports/course_activity.html',
                      {'form': form,
                       'course_activity': course_activity,
                       'previous_course_activity':
                       previous_course_activity,
                       'hot_courses': hot_courses})
