# oppia/views.py
import datetime

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, ListView

from helpers.forms.dates import DateRangeIntervalForm
from helpers.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from helpers.mixins.DateRangeFilterMixin import DateRangeFilterMixin
from helpers.mixins.SafePaginatorMixin import SafePaginatorMixin
from oppia import constants
from oppia import permissions
from oppia.models import Activity, Points
from oppia.models import Tracker, Participant, Course, CoursePermissions
from profile.models import UserProfile
from summary.models import CourseDailyStats, UserCourseSummary
from settings.models import SettingProperties

from settings import constants as settingconstants


class ServerView(TemplateView):
    content_type = 'application/json'
    template_name = 'oppia/server.html'
    extra_context = {'settings': settings}


class AboutView(TemplateView):
    template_name = 'oppia/about.html'
    extra_context = {'settings': settings}


class HomeView(DateRangeFilterMixin, TemplateView):
    template_name = 'oppia/home.html'
    daterange_form_class = DateRangeIntervalForm
    daterange_form_initial = {'interval': 'days'}

    def dispatch(self, request, *args, **kwargs):
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
                return HttpResponseRedirect(reverse('profile:user_activity', args=[request.user.id]))
            # is user is teacher redirect to teacher home
            if up.is_teacher_only():
                return HttpResponseRedirect(reverse('oppia:teacher_index'))

            if permissions.is_manager_only(request.user):
                return HttpResponseRedirect(reverse('oppia:manager_index'))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        start_date, end_date = self.get_daterange()
        interval = self.get_daterange_form().cleaned_data.get("interval")

        if interval == 'days':
            activity = process_home_activity_days(start_date, end_date)
        else:
            activity = process_home_activity_months(start_date, end_date)

        context['activity_graph_data_tracker_date'] = activity
        context['leaderboard'] = Points.get_leaderboard(constants.LEADERBOARD_HOMEPAGE_RESULTS_PER_PAGE)
        if SettingProperties.get_bool(settingconstants.OPPIA_ANDROID_ON_GOOGLE_PLAY, False):
            context['OPPIA_ANDROID_PACKAGEID'] = SettingProperties.get_string(settingconstants.OPPIA_ANDROID_PACKAGEID, '')
        return context


def process_home_activity_days(start_date, end_date):
    activity = []
    no_days = (end_date - start_date).days + 1
    tracker_stats = CourseDailyStats.objects \
        .filter(day__gte=start_date, day__lte=end_date) \
        .values('day') \
        .annotate(count=Sum('total'))

    for i in range(0, no_days, +1):
        temp = start_date + datetime.timedelta(days=i)
        count = next((dct['count']
                      for dct in tracker_stats
                      if dct['day'] == temp.date()), 0)
        activity.append([temp.strftime(constants.STR_DATE_DISPLAY_FORMAT),
                         count])
    return activity


def process_home_activity_months(start_date, end_date):
    activity = []
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


class ManagerView(TemplateView):

    template_name = 'oppia/home-manager.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        if not permissions.is_manager_only(self.request.user):
            raise PermissionDenied

        courses = Course.objects.filter(
            coursepermissions__user=self.request.user,
            coursepermissions__role=CoursePermissions.MANAGER)

        start_date = timezone.now() - datetime.timedelta(days=constants.ACTIVITY_GRAPH_DEFAULT_NO_DAYS)
        end_date = timezone.now()

        # get activity
        activity_tracker_date = get_trackers(start_date, end_date, courses, date_data="tracker_date")
        activity_submitted_date = get_trackers(start_date, end_date, courses, date_data="submitted_date")

        context['courses'] = courses
        context['activity_graph_data'] = activity_tracker_date
        context['activity_submitted_graph_data'] = activity_submitted_date

        return context


class TeacherView(TemplateView):
    template_name = 'oppia/home-teacher.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cohorts = permissions.get_cohorts(self.request)

        start_date = timezone.now() - datetime.timedelta(
            days=constants.ACTIVITY_GRAPH_DEFAULT_NO_DAYS)
        end_date = timezone.now()

        # get student activity
        students = User.objects \
            .filter(participant__role=Participant.STUDENT,
                    participant__cohort__in=cohorts).distinct()
        courses = Course.objects \
            .filter(coursecohort__cohort__in=cohorts).distinct()
        activity = get_trackers(start_date, end_date, courses, students)

        context['cohorts'] = cohorts
        context['activity_graph_data'] = activity
        return context


def get_trackers(start_date, end_date, courses, students=None, date_data='tracker_date'):
    activity = []
    no_days = (end_date - start_date).days + 1
    if date_data == "submitted_date":
        trackers = Tracker.objects.filter(course__in=courses,
                                          submitted_date__gte=start_date,
                                          submitted_date__lte=end_date)
    else:
        trackers = Tracker.objects.filter(course__in=courses, tracker_date__gte=start_date, tracker_date__lte=end_date)

    if students:
        trackers.filter(user__in=students)

    trackers.annotate(day=TruncDay(date_data), month=TruncMonth(date_data), year=TruncYear(date_data)) \
        .values('day') \
        .annotate(count=Count('id'))
    for i in range(0, no_days, +1):
        temp = start_date + datetime.timedelta(days=i)
        temp_date = temp.date().strftime(constants.STR_DATE_DISPLAY_FORMAT)
        count = next((dct['count']
                     for dct in trackers
                     if dct['day'].strftime(constants.STR_DATE_DISPLAY_FORMAT)
                     == temp_date), 0)
        activity.append([temp.strftime(constants.STR_DATE_DISPLAY_FORMAT),
                         count])
    return activity


class LeaderboardView(SafePaginatorMixin, ListView, AjaxTemplateResponseMixin):

    paginate_by = constants.LEADERBOARD_TABLE_RESULTS_PER_PAGE
    template_name = 'leaderboard/list.html'
    ajax_template_name = 'leaderboard/query.html'

    def get_queryset(self):
        return Points.get_leaderboard()


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
                if course.user_can_view(self.request.user):
                    context['course'] = course
                    context['download_stats'] = UserCourseSummary.objects \
                        .filter(course=course) \
                        .aggregated_stats('total_downloads', single=True)
                else:
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
