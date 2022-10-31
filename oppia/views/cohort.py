# oppia/views.py
import datetime
import operator

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.forms import formset_factory
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, UpdateView, DetailView
from django.views.generic.edit import FormView

from helpers.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from helpers.mixins.FormsetView import FormsetView
from helpers.mixins.PermissionMixins import StaffRequiredMixin
from helpers.mixins.SafePaginatorMixin import SafePaginatorMixin
from oppia import constants
from oppia.forms.cohort import CohortForm, CohortCriteriaForm
from oppia.models import Tracker, \
    CourseCohort, \
    Participant, \
    Course, \
    Cohort, CohortCritera
from oppia.permissions import can_add_cohort, \
    can_view_cohort, \
    can_edit_cohort
from oppia.views.utils import get_paginated_courses, filter_trackers
from profile.models import CustomField
from profile.utils import get_paginated_users
from summary.models import UserCourseSummary

STR_COHORT_TEMPLATE_FORM = 'cohort/form.html'

class CohortListView(StaffRequiredMixin, ListView):
    template_name = 'cohort/list.html'
    queryset = Cohort.objects.all()
    paginate_by = 20


def cohort_add_roles(cohort, role, users):
    user_list = users.strip().split(",")
    for u in user_list:
        try:
            participant = Participant()
            participant.cohort = cohort
            participant.user = User.objects.get(username=u.strip())
            participant.role = role
            participant.save()
        except User.DoesNotExist:
            pass


def cohort_add_courses(cohort, courses):
    course_list = courses.strip().split(",")
    for c in course_list:
        try:
            course = Course.objects.get(shortname=c.strip())
            CourseCohort(cohort=cohort, course=course).save()
        except Course.DoesNotExist:
            pass


class EditCohortMixin(FormsetView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applicable_criteria'] = CustomField.objects.all().exists()
        return context

    def get_named_formsets(self):
        return{
            'student_criteria': {'form': CohortCriteriaForm, 'kwargs': {'prefix': 'student'}},
            'teacher_criteria': {'form': CohortCriteriaForm, 'kwargs': {'prefix': 'teacher'}},
        }

    def formset_student_criteria_valid(self, form, formset):
        # Remove any previous cohort criteria to save the new ones
        CohortCritera.objects.filter(cohort=self.cohort, role=Participant.STUDENT).delete()
        for criteria_form in formset:
            self.save_criteria(criteria_form, Participant.STUDENT)

    def formset_teacher_criteria_valid(self, form, formset):
        # Remove any previous cohort criteria to save the new ones
        CohortCritera.objects.filter(cohort=self.cohort, role=Participant.TEACHER).delete()
        for criteria_form in formset:
            self.save_criteria(criteria_form, Participant.TEACHER)

    def get_criteria_initial(self, role):
        crits = []
        criteria = CohortCritera.objects.filter(cohort=self.cohort, role=role)
        for c in criteria:
            crits.append({
                'user_profile_field': c.user_profile_field,
                'user_profile_value': c.user_profile_value
            })
        return crits

    def save_criteria(self, criteria_form, role):
        field = criteria_form.cleaned_data.get('user_profile_field')
        value = criteria_form.cleaned_data.get('user_profile_value')
        if field and value:
            CohortCritera.objects.create(
                cohort=self.cohort, role=role,
                user_profile_field=field, user_profile_value=value
            )


class AddCohortView(FormView, UserPassesTestMixin, EditCohortMixin):
    template_name = STR_COHORT_TEMPLATE_FORM
    success_url = reverse_lazy('oppia:cohorts')
    form_class = CohortForm

    # Permissions check
    def test_func(self):
        return can_add_cohort(self.request)

    def form_valid(self, form):
        cohort = Cohort(
            description=form.cleaned_data.get("description").strip(),
            criteria_based=form.cleaned_data.get('criteria_based'),
            last_updated=datetime.datetime.now()
        )
        cohort.save()
        self.cohort = cohort

        students = form.cleaned_data.get("students")
        cohort_add_roles(cohort, Participant.STUDENT, students)

        teachers = form.cleaned_data.get("teachers")
        cohort_add_roles(cohort, Participant.TEACHER, teachers)

        courses = form.cleaned_data.get("courses")
        cohort_add_courses(cohort, courses)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ordering, users = get_paginated_users(self.request)
        c_ordering, courses = get_paginated_courses(self.request)
        context['is_new'] = True,
        context['page'] = users
        context['courses_page'] = courses
        context['courses_ordering'] = c_ordering
        context['page_ordering'] = ordering
        context['users_list_template'] = 'select'

        return context


class CohortDetailView(UserPassesTestMixin, DetailView):
    template_name = 'cohort/activity.html'
    model = Cohort
    context_object_name = 'cohort'

    # Permissions check
    def test_func(self):
        return can_view_cohort(self.request, self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date = timezone.now() - datetime.timedelta(
            days=constants.ACTIVITY_GRAPH_DEFAULT_NO_DAYS)
        end_date = timezone.now()

        # get student activity
        students = User.objects.filter(participant__role=Participant.STUDENT,
                                       participant__cohort=self.object)
        trackers = Tracker.objects.filter(
            course__coursecohort__cohort=self.object,
            user__is_staff=False,
            user__in=students)
        context['activity_graph_data'] = filter_trackers(trackers, start_date, end_date)
        context['leaderboard'] = self.object.get_leaderboard(
            constants.LEADERBOARD_HOMEPAGE_RESULTS_PER_PAGE)

        return context


class CohortLeaderboardView(UserPassesTestMixin,
                            SafePaginatorMixin,
                            ListView,
                            AjaxTemplateResponseMixin):

    paginate_by = constants.LEADERBOARD_TABLE_RESULTS_PER_PAGE
    template_name = 'cohort/leaderboard.html'
    ajax_template_name = 'leaderboard/query.html'

    # Permissions check
    def test_func(self):
        return can_view_cohort(self.request, self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        self.object = Cohort.objects.get(pk=kwargs['pk'])
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.get_leaderboard()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cohort'] = self.object
        return context


class CohortEditView(UserPassesTestMixin, UpdateView, EditCohortMixin):
    template_name = STR_COHORT_TEMPLATE_FORM
    model = Cohort
    form_class = CohortForm

    # Permissions check
    def test_func(self):
        return can_edit_cohort(self.request)

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {'initial': self.get_initial()}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_initial(self):
        self.cohort = self.object
        return {
            'description': self.object.description,
            'start_date': self.object.start_date,
            'end_date': self.object.end_date,
            'criteria_based': self.object.criteria_based
        }

    def formset_student_criteria_get_initial(self):
        return self.get_criteria_initial(Participant.STUDENT)

    def formset_teacher_criteria_get_initial(self):
        return self.get_criteria_initial(Participant.TEACHER)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['selected_teachers'] = User.objects.filter(
            participant__role=Participant.TEACHER,
            participant__cohort=self.object)
        context['selected_students'] = User.objects.filter(
            participant__role=Participant.STUDENT,
            participant__cohort=self.object)
        context['selected_courses'] = Course.objects.filter(
            coursecohort__cohort=self.object)

        ordering, users = get_paginated_users(self.request)
        c_ordering, courses = get_paginated_courses(self.request)

        context.update({
            'page': users,
            'courses_page': courses,
            'courses_ordering': c_ordering,
            'page_ordering': ordering,
            'users_list_template': 'select'
        })
        return context

    def get_success_url(self):
        return reverse('oppia:cohorts')

    def form_valid(self, form):
        cohort = self.object
        self.cohort = cohort
        cohort.description = form.cleaned_data.get("description").strip()
        cohort.criteria_based = form.cleaned_data.get('criteria_based')
        start_date = form.cleaned_data.get("start_date")
        end_date = form.cleaned_data.get("end_date")
        if start_date:
            cohort.start_date = timezone.make_aware(
                datetime.datetime.strptime(
                    start_date,
                    constants.STR_DATE_FORMAT),
                timezone.get_current_timezone())
        else:
            cohort.start_date = None

        if end_date:
            cohort.end_date = timezone.make_aware(
                datetime.datetime.strptime(
                    end_date,
                    constants.STR_DATE_FORMAT),
                timezone.get_current_timezone())
        else:
            cohort.end_date = None

        cohort.last_updated = datetime.datetime.now()
        cohort.save()

        Participant.objects.filter(cohort=cohort).delete()
        students = form.cleaned_data.get("students")
        cohort_add_roles(cohort, Participant.STUDENT, students)
        teachers = form.cleaned_data.get("teachers")
        cohort_add_roles(cohort, Participant.TEACHER, teachers)

        CourseCohort.objects.filter(cohort=cohort).delete()
        courses = form.cleaned_data.get("courses")
        cohort_add_courses(cohort, courses)

        return super().form_valid(form)


def cohort_course_view(request, cohort_id, course_id):
    cohort = can_view_cohort(request, cohort_id)

    try:
        course = Course.objects.get(pk=course_id, coursecohort__cohort=cohort)
    except Course.DoesNotExist:
        raise Http404()

    start_date = timezone.now() - datetime.timedelta(
            days=constants.ACTIVITY_GRAPH_DEFAULT_NO_DAYS)
    end_date = timezone.now()

    users = User.objects.filter(
        participant__role=Participant.STUDENT,
        participant__cohort=cohort).order_by('first_name', 'last_name')
    trackers = Tracker.objects.filter(course=course,
                                      user__is_staff=False,
                                      user__in=users)

    student_activity = filter_trackers(trackers, start_date, end_date)

    students = []
    media_count = course.get_no_media()
    for user in users:
        course_stats = UserCourseSummary.objects.filter(user=user,
                                                        course=course_id)
        if course_stats:
            course_stats = course_stats[0]
            if course_stats.pretest_score:
                pretest_score = course_stats.pretest_score
            else:
                pretest_score = 0
            data = {'user': user,
                    'user_display': str(user),
                    'no_quizzes_completed': course_stats.quizzes_passed,
                    'pretest_score': round(pretest_score, 1),
                    'no_activities_completed':
                        course_stats.completed_activities,
                    'no_points': course_stats.points,
                    'no_badges': course_stats.badges_achieved,
                    'no_media_viewed': course_stats.media_viewed}
        else:
            # The user has no activity registered
            data = {'user': user,
                    'user_display': str(user),
                    'no_quizzes_completed': 0,
                    'pretest_score': 0,
                    'no_activities_completed': 0,
                    'no_points': 0,
                    'no_badges': 0,
                    'no_media_viewed': 0}

        students.append(data)

    order_options = ['user_display',
                     'no_quizzes_completed',
                     'pretest_score',
                     'no_activities_completed',
                     'no_points',
                     'no_badges',
                     'no_media_viewed']
    default_order = 'pretest_score'

    ordering = request.GET.get('order_by', default_order)
    inverse_order = ordering.startswith('-')
    if inverse_order:
        ordering = ordering[1:]

    if ordering not in order_options:
        ordering = default_order
        inverse_order = False

    students.sort(key=operator.itemgetter(ordering), reverse=inverse_order)

    return render(request, 'cohort/course-activity.html',
                  {'course': course,
                   'cohort': cohort,
                   'course_media_count': media_count,
                   'activity_graph_data': student_activity,
                   'page_ordering': ('-' if inverse_order else '') + ordering,
                   'students': students})
