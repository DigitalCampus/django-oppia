import json

import tablib
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView, ListView

from helpers.forms.dates import DateRangeIntervalForm
from helpers.mixins.DateRangeFilterMixin import DateRangeFilterMixin
from helpers.mixins.SafePaginatorMixin import SafePaginatorMixin
from oppia import constants
from oppia.forms.activity_search import ActivitySearchForm
from oppia.models import Points, Course
from oppia.models import Tracker
from oppia.permissions import can_view_course_detail, can_edit_course_gamification
from oppia.views.utils import generate_graph_data
from profile import utils
from summary.models import CourseDailyStats, UserCourseSummary


class CourseActivityDetail(DateRangeFilterMixin, DetailView):
    template_name = 'course/detail.html'
    pk_url_kwarg = 'course_id'
    context_object_name = 'course'
    model = Course
    daterange_form_class = DateRangeIntervalForm
    daterange_form_initial = {'interval': 'days'}

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        can_view_course_detail(self.request, self.object.id)

        start_date, end_date = self.get_daterange()
        interval = self.get_daterange_form().cleaned_data.get("interval")
        context['monthly'] = interval == 'months'

        context['download_stats'] = UserCourseSummary.objects \
            .filter(course=self.object.id).aggregated_stats('total_downloads', single=True)
        context['leaderboard'] = Points.get_leaderboard(constants.LEADERBOARD_HOMEPAGE_RESULTS_PER_PAGE, self.object)
        context['data'] = self.get_activity(start_date, end_date, interval)
        context['can_edit_course_gamification'] = can_edit_course_gamification(self.request, self.object.id)

        return context

    def get_activity(self, start_date, end_date, interval):
        if interval == 'days':
            daily_stats = CourseDailyStats.objects\
                .filter(course=self.object, day__gte=start_date, day__lte=end_date) \
                .annotate(stat_date=TruncDay('day')) \
                .values('stat_date', 'type') \
                .annotate(total=Sum('total'))

            return generate_graph_data(daily_stats, False)

        else:
            monthly_stats = CourseDailyStats.objects \
                .filter(course=self.object, day__gte=start_date, day__lte=end_date) \
                .annotate(month=TruncMonth('day'), year=TruncYear('day')) \
                .values('month', 'year', 'type') \
                .annotate(total=Sum('total')) \
                .order_by('year', 'month')

            return generate_graph_data(monthly_stats, True)


class CourseActivityDetailList(DateRangeFilterMixin, SafePaginatorMixin, ListView):
    template_name = 'course/activity/list.html'
    paginate_by = 25
    daterange_form_class = ActivitySearchForm

    def get_course_id(self):
        return self.kwargs['course_id']

    def get_queryset(self):
        self.filtered = False
        trackers = Tracker.objects.filter(course__pk=self.get_course_id())
        start_date, end_date = self.get_daterange()
        trackers = trackers.filter(tracker_date__gte=start_date, tracker_date__lte=end_date)

        filters = utils.get_filters_from_row(self.get_daterange_form(), convert_date=False)
        if filters:
            trackers = trackers.filter(**filters)
            self.filtered = True

        return trackers.order_by('-tracker_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = can_view_course_detail(self.request, self.get_course_id())
        context['advanced_search'] = self.filtered

        for tracker in context['page_obj'].object_list:
            tracker.data_obj = []
            try:
                data_dict = json.loads(tracker.data)
                for key, value in data_dict.items():
                    tracker.data_obj.append([key, value])
            except ValueError:
                pass
            tracker.data_obj.append(['agent', tracker.agent])
            tracker.data_obj.append(['ip', tracker.ip])

        return context


class ExportCourseTrackers(TemplateView):

    def get(self, request, course_id):
        course = can_view_course_detail(request, course_id)

        headers = ('Date',
                   'UserId',
                   'Type',
                   'Activity Title',
                   'Section Title',
                   'Time Taken',
                   'IP Address',
                   'User Agent',
                   'Language')
        data = []
        data = tablib.Dataset(* data, headers=headers)
        trackers = Tracker.objects.filter(course=course) \
            .order_by('-tracker_date')
        for t in trackers:
            try:
                data_dict = json.loads(t.data)
                if 'lang' in data_dict:
                    lang = data_dict['lang']
                else:
                    lang = ""
                data.append((t.tracker_date.strftime(
                    constants.STR_DATETIME_FORMAT),
                             t.user.id,
                             t.type,
                             t.get_activity_title(),
                             t.get_section_title(),
                             t.time_taken,
                             t.ip,
                             t.agent,
                             lang))
            except ValueError:
                try:
                    data.append((t.tracker_date.strftime(
                        constants.STR_DATETIME_FORMAT),
                                 t.user.id,
                                 t.type,
                                 "",
                                 "",
                                 t.time_taken,
                                 t.ip,
                                 t.agent,
                                 ""))
                except User.DoesNotExist:
                    pass

        response = HttpResponse(
            data.export('xlsx'),
            content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=export.xlsx"

        return response
