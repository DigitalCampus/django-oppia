import datetime

from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncYear

from oppia.test import OppiaTestCase

from oppia.models import Course
from oppia.views.utils import generate_graph_data
from summary.models import CourseDailyStats


class OppiaViewUtilsTest(OppiaTestCase):
    
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_permissions.json',
                'tests/test_coursedailystats.json',
                'default_badges.json']
    
    def test_graph_data_daily(self):
        course = Course.objects.get(pk=1)
        
        start_date = datetime.datetime(2017, 1, 1)
        end_date = datetime.datetime(2017, 12, 31)
        daily_stats = CourseDailyStats.objects.filter(course=course,
                                                          day__gte=start_date,
                                                          day__lte=end_date) \
                            .annotate(stat_date=TruncDay('day')) \
                            .values('stat_date', 'type') \
                            .annotate(total=Sum('total'))
        result = generate_graph_data(daily_stats)
        self.assertEqual(34, len(result))
        
    def test_graph_data_monthly(self):
        course = Course.objects.get(pk=1)
        
        start_date = datetime.datetime(2017, 1, 1)
        end_date = datetime.datetime(2017, 12, 31)
        monthly_stats = CourseDailyStats.objects \
                .filter(course=course,
                        day__gte=start_date,
                        day__lte=end_date) \
                .annotate(month=TruncMonth('day'),
                          year=TruncYear('day')) \
                .values('month', 'year', 'type') \
                .annotate(total=Sum('total')) \
                .order_by('year', 'month')
        result = generate_graph_data(monthly_stats, True)
        self.assertEqual(10, len(result))
        