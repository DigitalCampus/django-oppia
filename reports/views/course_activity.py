import datetime

from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from oppia.models import Course
from reports.views.base_report_template import BaseReportTemplateView
from summary.models import CourseDailyStats


class CourseActivityView(BaseReportTemplateView):

    template_name = 'reports/course_activity.html'

    def get_graph_data(self, start_date, end_date):

        daily_activity = CourseDailyStats.objects \
            .filter(day__gte=start_date, day__lte=end_date) \
            .values('day') \
            .annotate(count=Sum('total')) \
            .order_by('day')

        course_activity = CourseDailyStats.objects \
            .filter(day__gte=start_date, day__lte=end_date) \
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
        return  {
            'daily_activity': daily_activity,
            'course_activity': course_activity,
            'previous_course_activity': previous_course_activity,
            'hot_courses': hot_courses
        }
