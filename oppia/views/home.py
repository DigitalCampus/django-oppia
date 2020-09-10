# oppia/views.py
import datetime

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView

from helpers.forms.dates import DateRangeIntervalForm
from oppia.models import Activity, Points
from oppia.models import Tracker, \
    Participant, \
    Course
from oppia import permissions
from reports.signals import dashboard_accessed
from summary.models import CourseDailyStats, UserCourseSummary

from profile.models import UserProfile

STR_DATE_FORMAT = "%d %b %Y"


def server_view(request):
    return render(request, 'oppia/server.html',
                  {'settings': settings},
                  content_type="application/json")


def about_view(request):
    return render(request, 'oppia/about.html',
                  {'settings': settings})


def home_view(request):

    if request.user.is_authenticated:

        # create profile if none exists (for first admin user login and
        # historical for very old users)
        try:
            request.user.userprofile
        except UserProfile.DoesNotExist:
            up = UserProfile()
            up.user = request.user
            up.save()

        up = request.user.userprofile
        # if user is student redirect to their scorecard
        if up.is_student_only():
            return HttpResponseRedirect(reverse('profile:user_activity',
                                                args=[request.user.id]))

        # is user is teacher redirect to teacher home
        if up.is_teacher_only():
            return HttpResponseRedirect(reverse('oppia:teacher_index'))

        # admin/staff view
        form, activity = home_view_admin_authenticated(request)
        leaderboard = Points.get_leaderboard(10)
    else:
        activity = []
        leaderboard = None
        form = None

    return render(request, 'oppia/home.html',
                  {'form': form,
                   'activity_graph_data': activity,
                   'leaderboard': leaderboard})


def home_view_admin_authenticated(request):
    activity = []

    dashboard_accessed.send(sender=None, request=request, data=None)

    start_date = timezone.now() - datetime.timedelta(days=31)
    end_date = timezone.now()
    interval = 'days'
    if request.method == 'POST':
        form = DateRangeIntervalForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get("start_date")
            start_date = datetime.datetime.strptime(start_date,
                                                    "%Y-%m-%d")
            end_date = form.cleaned_data.get("end_date")
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            interval = form.cleaned_data.get("interval")
    else:
        data = {}
        data['start_date'] = start_date
        data['end_date'] = end_date
        data['interval'] = interval
        form = DateRangeIntervalForm(initial=data)

    if interval == 'days':
        activity = process_home_activity_days(activity, start_date, end_date)
    else:
        activity = process_home_activity_months(activity, start_date, end_date)

    return form, activity


def process_home_activity_days(activity, start_date, end_date):
    no_days = (end_date - start_date).days + 1
    tracker_stats = CourseDailyStats.objects \
        .filter(day__gte=start_date,
                day__lte=end_date) \
        .values('day') \
        .annotate(count=Sum('total'))

    for i in range(0, no_days, +1):
        temp = start_date + datetime.timedelta(days=i)
        count = next((dct['count']
                      for dct in tracker_stats
                      if dct['day'] == temp.date()), 0)
        activity.append([temp.strftime(STR_DATE_FORMAT), count])
    return activity


def process_home_activity_months(activity, start_date, end_date):
    delta = relativedelta(months=+1)

    no_months = 0
    tmp_date = start_date
    while tmp_date <= end_date:
        tmp_date += delta
        no_months += 1

    for i in range(0, no_months, +1):
        temp = start_date + relativedelta(months=+i)
        month = temp.strftime("%m")
        year = temp.strftime("%Y")
        count = CourseDailyStats.objects \
            .filter(day__month=month, day__year=year) \
            .aggregate(total=Sum('total')).get('total', 0)
        activity.append([temp.strftime("%b %Y"),
                         0 if count is None else count])
    return activity


def teacher_home_view(request):
    cohorts = permissions.get_cohorts(request)

    start_date = timezone.now() - datetime.timedelta(days=31)
    end_date = timezone.now()

    # get student activity
    activity = []
    no_days = (end_date - start_date).days + 1
    students = User.objects \
        .filter(participant__role=Participant.STUDENT,
                participant__cohort__in=cohorts).distinct()
    courses = Course.objects \
        .filter(coursecohort__cohort__in=cohorts).distinct()
    trackers = Tracker.objects.filter(course__in=courses,
                                      user__in=students,
                                      tracker_date__gte=start_date,
                                      tracker_date__lte=end_date) \
        .annotate(day=TruncDay('tracker_date'),
                  month=TruncMonth('tracker_date'),
                  year=TruncYear('tracker_date')) \
        .values('day') \
        .annotate(count=Count('id'))
    for i in range(0, no_days, +1):
        temp = start_date + datetime.timedelta(days=i)
        temp_date = temp.date().strftime(STR_DATE_FORMAT)
        count = next((dct['count']
                     for dct in trackers
                     if dct['day'].strftime(STR_DATE_FORMAT) == temp_date), 0)
        activity.append([temp.strftime(STR_DATE_FORMAT), count])

    dashboard_accessed.send(sender=None, request=request, data=None)

    return render(request, 'oppia/home-teacher.html',
                  {'cohorts': cohorts,
                   'activity_graph_data': activity, })


def leaderboard_view(request):
    lb = Points.get_leaderboard()
    paginator = Paginator(lb, 25)  # Show 25 per page

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        leaderboard = paginator.page(page)
    except (EmptyPage, InvalidPage):
        leaderboard = paginator.page(paginator.num_pages)

    return render(request, 'oppia/leaderboard.html', {'page': leaderboard})


class AppLauncherDetailView(TemplateView):

    template_name = 'course/app_launcher.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        digest = self.request.GET.get('digest')
        course_shortname = self.request.GET.get('course')

        if digest:
            context['digest'] = digest
            activity = Activity.objects.filter(digest=digest).first()
            if activity:
                context['activity'] = activity
            else:
                context['misconfigured'] = True
                context['activity_notfound'] = True

        elif course_shortname:
            context['course_shortname'] = course_shortname
            course = Course.objects.filter(shortname=course_shortname).first()
            if course:
                try:
                    permissions.can_view_course(self.request, course.id)
                    context['course'] = course
                    context['download_stats'] = UserCourseSummary.objects \
                        .filter(course=course) \
                        .aggregated_stats('total_downloads', single=True)

                except Http404:
                    # The user does not have permissions to view this course
                    context['misconfigured'] = True
                    context['course_notpermissions'] = True

            else:
                context['misconfigured'] = True
                context['course_notfound'] = True
        else:
            context['misconfigured'] = True
            context['param_missing'] = True

        return context
