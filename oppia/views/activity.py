import datetime
import json

import tablib
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from helpers.forms.dates import DateRangeIntervalForm, DateRangeForm
from oppia.models import Points
from oppia.models import Tracker
from oppia.permissions import can_view_course_detail
from oppia.views.utils import generate_graph_data
from reports.signals import dashboard_accessed
from summary.models import CourseDailyStats, UserCourseSummary


class CourseActivityDetail(TemplateView):

    def get(self, request, course_id):

        course = can_view_course_detail(request, course_id)

        dashboard_accessed.send(sender=None, request=request, data=course)

        start_date = datetime.datetime.now() - datetime.timedelta(days=31)
        end_date = datetime.datetime.now()
        interval = 'days'

        return self.process(request, course, start_date, end_date, interval)

    def post(self, request, course_id):

        course = can_view_course_detail(request, course_id)

        dashboard_accessed.send(sender=None, request=request, data=course)

        form = DateRangeIntervalForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get("start_date")
            start_date = datetime.datetime.strptime(start_date + " 00:00:00",
                                                    "%Y-%m-%d %H:%M:%S")
            end_date = form.cleaned_data.get("end_date")
            end_date = datetime.datetime.strptime(end_date + " 23:59:59",
                                                  "%Y-%m-%d %H:%M:%S")
            interval = form.cleaned_data.get("interval")
        else:
            start_date = datetime.datetime.now() - datetime.timedelta(days=31)
            end_date = datetime.datetime.now()
            interval = 'days'

        return self.process(request, course, start_date, end_date, interval)

    def process(self, request, course, start_date, end_date, interval):

        download_stats = UserCourseSummary.objects \
            .filter(course=course.id) \
            .aggregated_stats('total_downloads', single=True)

        data = {}
        data['start_date'] = start_date
        data['end_date'] = end_date
        data['interval'] = interval
        form = DateRangeIntervalForm(initial=data)

        dates = []
        if interval == 'days':
            daily_stats = CourseDailyStats.objects.filter(course=course,
                                                          day__gte=start_date,
                                                          day__lte=end_date) \
                            .annotate(stat_date=TruncDay('day')) \
                            .values('stat_date', 'type') \
                            .annotate(total=Sum('total'))

            dates = generate_graph_data(daily_stats, False)

        else:
            monthly_stats = CourseDailyStats.objects \
                .filter(course=course,
                        day__gte=start_date,
                        day__lte=end_date) \
                .annotate(month=TruncMonth('day'),
                          year=TruncYear('day')) \
                .values('month', 'year', 'type') \
                .annotate(total=Sum('total')) \
                .order_by('year', 'month')

            dates = generate_graph_data(monthly_stats, True)

        leaderboard = Points.get_leaderboard(10, course)

        return render(request, 'course/detail.html',
                      {'course': course,
                       'monthly': interval == 'months',
                       'form': form,
                       'data': dates,
                       'download_stats': download_stats,
                       'leaderboard': leaderboard})


class CourseRecentActivityDetail(TemplateView):

    def get(self, request, course_id):
        course = can_view_course_detail(request, course_id)

        start_date = datetime.datetime.now() - datetime.timedelta(days=31)
        end_date = datetime.datetime.now()

        data = {}
        data['start_date'] = start_date
        data['end_date'] = end_date
        form = DateRangeForm(initial=data)

        return self.process(request,
                            course,
                            form,
                            start_date,
                            end_date)

    def post(self, request, course_id):
        course = can_view_course_detail(request, course_id)

        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get("start_date")
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_date = form.cleaned_data.get("end_date")
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        else:
            start_date = datetime.datetime.now() - datetime.timedelta(days=31)
            end_date = datetime.datetime.now()

        return self.process(request,
                            course,
                            form,
                            start_date,
                            end_date)

    def process(self, request, course, form, start_date, end_date):
        data = {}
        data['start_date'] = start_date
        data['end_date'] = end_date
        trackers = Tracker.objects.filter(course=course,
                                          tracker_date__gte=start_date,
                                          tracker_date__lte=end_date) \
                          .order_by('-tracker_date')

        paginator = Paginator(trackers, 25)
        # Make sure page request is an int. If not, deliver first page.
        try:
            page = int(request.GET.get('page', '1'))
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

        return render(request, 'course/activity-detail.html',
                      {'course': course,
                       'form': form,
                       'page': tracks, })


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
                data.append((t.tracker_date.strftime('%Y-%m-%d %H:%M:%S'),
                             t.user.id,
                             t.type,
                             t.get_activity_title(),
                             t.get_section_title(),
                             t.time_taken,
                             t.ip,
                             t.agent,
                             lang))
            except ValueError:
                data.append((t.tracker_date.strftime('%Y-%m-%d %H:%M:%S'),
                             t.user.id,
                             t.type,
                             "",
                             "",
                             t.time_taken,
                             t.ip,
                             t.agent,
                             ""))

        response = HttpResponse(
            data.export('xlsx'),
            content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=export.xlsx"

        return response
