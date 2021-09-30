import datetime
import json

import tablib
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView, DetailView

from helpers.forms.dates import DateRangeIntervalForm, DateRangeForm
from oppia import constants
from oppia.models import Points, Course
from oppia.models import Tracker
from oppia.permissions import can_view_course_detail
from oppia.views.utils import generate_graph_data
from summary.models import CourseDailyStats, UserCourseSummary


class CourseActivityDetail(DetailView):

    template_name = 'course/detail.html'
    pk_url_kwarg = 'course_id'
    context_object_name = 'course'
    model = Course

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        can_view_course_detail(self.request, self.object.id)

        start_date = timezone.now() - datetime.timedelta(
            days=constants.ACTIVITY_GRAPH_DEFAULT_NO_DAYS)
        end_date = timezone.now()
        interval = 'days'
        initial = {'start_date': start_date,
                   'end_date': end_date,
                   'interval': interval}

        initial.update(self.request.GET.dict())
        if isinstance(initial['interval'], list):
            initial['interval'] = initial['interval'][0]

        form = DateRangeIntervalForm(initial)
        if form.is_valid():
            start_date = timezone.make_aware(
                datetime.datetime.strptime(form.cleaned_data.get("start_date"),
                                           constants.STR_DATE_FORMAT),
                timezone.get_current_timezone())
            end_date = timezone.make_aware(
                datetime.datetime.strptime(form.cleaned_data.get("end_date"),
                                           constants.STR_DATE_FORMAT),
                timezone.get_current_timezone())
            interval = form.cleaned_data.get("interval")

        form.form_method = 'get'
        context['form'] = form
        context['monthly'] = interval == 'months'

        context['download_stats'] = UserCourseSummary.objects \
            .filter(course=self.object.id) \
            .aggregated_stats('total_downloads', single=True)

        context['leaderboard'] = Points.get_leaderboard(
            constants.LEADERBOARD_HOMEPAGE_RESULTS_PER_PAGE, self.object)

        context['data'] = self.get_activity(start_date, end_date, interval)

        return context

    def get_activity(self, start_date, end_date, interval):
        if interval == 'days':
            daily_stats = CourseDailyStats.objects\
                .filter(course=self.object,
                        day__gte=start_date,
                        day__lte=end_date) \
                .annotate(stat_date=TruncDay('day')) \
                .values('stat_date', 'type') \
                .annotate(total=Sum('total'))

            return generate_graph_data(daily_stats, False)

        else:
            monthly_stats = CourseDailyStats.objects \
                .filter(course=self.object,
                        day__gte=start_date,
                        day__lte=end_date) \
                .annotate(month=TruncMonth('day'), year=TruncYear('day')) \
                .values('month', 'year', 'type') \
                .annotate(total=Sum('total')) \
                .order_by('year', 'month')

            return generate_graph_data(monthly_stats, True)


class CourseRecentActivityDetail(DetailView):

    template_name = 'course/activity-detail.html'
    pk_url_kwarg = 'course_id'
    context_object_name = 'course'
    model = Course

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        can_view_course_detail(self.request, self.object.id)

        start_date = timezone.now() - datetime.timedelta(
            days=constants.ACTIVITY_GRAPH_DEFAULT_NO_DAYS)
        end_date = timezone.now()
        initial = {'start_date': start_date, 'end_date': end_date}
        initial.update(self.request.GET.dict())

        form = DateRangeForm(initial)
        if form.is_valid():
            start_date = timezone.make_aware(
                datetime.datetime.strptime(form.cleaned_data.get("start_date"),
                                           constants.STR_DATE_FORMAT),
                timezone.get_current_timezone())
            end_date = timezone.make_aware(
                datetime.datetime.strptime(form.cleaned_data.get("end_date"),
                                           constants.STR_DATE_FORMAT),
                timezone.get_current_timezone())

        form.form_method = 'get'
        context['form'] = form
        context['page'] = self.get_activitylogs_page(start_date, end_date)
        return context

    def get_activitylogs_page(self, start_date, end_date):

        trackers = Tracker.objects.filter(course=self.object,
                                          tracker_date__gte=start_date,
                                          tracker_date__lte=end_date) \
                          .order_by('-tracker_date')

        paginator = Paginator(trackers,
                              constants.LEADERBOARD_TABLE_RESULTS_PER_PAGE)
        # Make sure page request is an int. If not, deliver first page.
        try:
            page = int(self.request.GET.get('page', '1'))
        except ValueError:
            page = 1

        # If page request (9999) is out of range, deliver last page of results.
        try:
            tracks = paginator.page(page)
            for t in tracks:

                t.data_obj = []
                try:
                    data_dict = json.loads(t.data)
                    for key, value in data_dict.items():
                        t.data_obj.append([key, value])
                except ValueError:
                    pass
                t.data_obj.append(['agent', t.agent])
                t.data_obj.append(['ip', t.ip])
        except (EmptyPage, InvalidPage):
            tracks = paginator.page(paginator.num_pages)

        return tracks


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
