# oppia/permissions.py
import functools
from itertools import chain

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404

from oppia.models import Course, Participant, Cohort, CoursePermissions
from oppia.utils.filters import CourseFilter
from profile.models import UserProfile


def can_upload(user):
    if user.is_superuser or user.is_staff:
        return True
    else:
        try:
            profile = UserProfile.objects.get(user=user)
            return profile.get_can_upload()
        except UserProfile.DoesNotExist:
            return False


def user_can_upload(function):
    def wrap(request, *args, **kwargs):
        if can_upload(request.user):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


def can_edit_user(request, view_user_id):
    if request.user.is_staff or request.user.id == view_user_id:
        return True
    else:
        return False


def get_user_courses(request, view_user):

    if request.user.is_staff or request.user == view_user:
        # get all courses user has taken part in
        # plus all those they are students on
        cohort_courses = Course.objects.filter(
            coursecohort__cohort__participant__user=view_user,
            coursecohort__cohort__participant__role=Participant.STUDENT
            ).distinct().order_by('title')
        other_courses = Course.objects.filter(tracker__user=view_user) \
            .exclude(pk__in=cohort_courses.values_list('id', flat=True)) \
            .distinct().order_by('title')
    else:
        cohort_courses = Course.objects.filter(
            coursecohort__cohort__participant__user=view_user,
            coursecohort__cohort__participant__role=Participant.STUDENT) \
            .filter(
                coursecohort__cohort__participant__user=request.user,
                coursecohort__cohort__participant__role=Participant.TEACHER) \
            .distinct().order_by('title')
        other_courses = Course.objects.none()

    all_courses = list(chain(cohort_courses, other_courses))
    return cohort_courses, other_courses, all_courses


def is_manager_only(user):
    # check only the owner can view
    if user.is_staff:
        return False
    else:
        courses = Course.objects.filter(user=user)
        if courses.exists():
            return True

        courses = Course.objects.filter(
            coursepermissions__user=user,
            coursepermissions__role=CoursePermissions.MANAGER)
        if courses.exists():
            return True
    return False


def permission_edit_cohort(view_func):
    """
        this decorator ensures that only the users who have permission to
        view a course can view it, raising a 403 otherwise
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def permission_view_cohort(view_func):
    """
        this decorator ensures that only the users who have permission to
        view a course can view it, raising a 403 otherwise
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        get_object_or_404(Cohort, pk=kwargs['cohort_id'])
        if not request.user.is_staff:
            cohort = Cohort.objects.filter(pk=kwargs['cohort_id'],
                                           participant__user=request.user,
                                           participant__role=Participant.TEACHER)
            if not cohort.exists():
                raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def get_cohorts(request):
    if request.user.is_staff:
        cohorts = Cohort.objects.all().order_by('description')
    else:
        cohorts = Cohort.objects.filter(
            participant__user=request.user,
            participant__role=Participant.TEACHER).order_by('description')

    if cohorts.count() == 0:
        raise PermissionDenied

    return cohorts


def can_download_course(request, course_id):
    try:
        if request.user.is_staff:
            course = Course.objects.filter(CourseFilter.IS_NOT_ARCHIVED).get(pk=course_id)
        else:
            try:
                course = Course.objects \
                    .filter(CourseFilter.IS_NOT_DRAFT
                            & CourseFilter.IS_NOT_ARCHIVED
                            & CourseFilter.NEW_DOWNLOADS_ENABLED) \
                    .filter(CourseFilter.get_restricted_filter_for_user(request.user)) \
                    .get(pk=course_id)

            except Course.DoesNotExist:
                course = Course.objects \
                    .filter(CourseFilter.IS_NOT_ARCHIVED) \
                    .get(pk=course_id,
                         coursepermissions__course__id=course_id,
                         coursepermissions__user__id=request.user.id,
                         coursepermissions__role=CoursePermissions.VIEWER)
    except Course.DoesNotExist:
        raise Http404
    return course


def permission_view_course(view_func):
    """
        this decorator ensures that only the users who have permission to
        view a course can view it, raising a 403 otherwise
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['course_id'])
        if not course.user_can_view(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def permission_view_course_detail(view_func):
    """
        this decorator ensures that only the users who have permission to
        access a course detail can view it, raising a 403 otherwise
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['course_id'])
        if not course.user_can_view_detail(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def can_view_course_activity(request, course_id):
    try:
        if request.user.is_staff:
            return Course.objects.filter(pk=course_id).exists()
        else:
            try:
                return Course.objects \
                    .filter(CourseFilter.IS_NOT_DRAFT & CourseFilter.IS_NOT_ARCHIVED) \
                    .filter(CourseFilter.get_restricted_filter_for_user(request.user)) \
                    .filter(pk=course_id).exists()
            except Course.DoesNotExist:
                return Course.objects \
                    .filter(CourseFilter.IS_NOT_ARCHIVED & CourseFilter.IS_NOT_DRAFT) \
                    .filter(
                        pk=course_id,
                        coursepermissions__course__id=course_id,
                        coursepermissions__user__id=request.user.id,
                        coursepermissions__role=CoursePermissions.VIEWER).exists()
    except Course.DoesNotExist:
        return False


def can_edit_course(request, course_id):
    if request.user.is_staff:
        return True
    else:
        try:
            Course.objects.get(
                pk=course_id,
                coursepermissions__course__id=course_id,
                coursepermissions__user=request.user,
                coursepermissions__role=CoursePermissions.MANAGER)
            return True
        except Course.DoesNotExist:
            return False


def can_view_courses_list(request, order_by='title'):
    if request.user.is_staff:
        courses = Course.objects.all().order_by(order_by)
    else:
        manager_courses = Course.objects.filter(
            coursepermissions__user=request.user,
            coursepermissions__role=CoursePermissions.MANAGER) \
            .order_by(order_by)
        if manager_courses.exists():
            return manager_courses

        courses = Course.objects\
            .filter(CourseFilter.IS_NOT_DRAFT & CourseFilter.IS_NOT_ARCHIVED) \
            .filter(CourseFilter.get_restricted_filter_for_user(request.user)) \
            .order_by(order_by)
    return courses


def can_edit_course_gamification(request, course_id):
    return can_edit_course(request, course_id) \
           and Course.objects.filter(CourseFilter.IS_NOT_ARCHIVED
                                     & CourseFilter.NEW_DOWNLOADS_ENABLED
                                     & CourseFilter.IS_NOT_READ_ONLY).filter(pk=course_id).exists()


# Sonarcloud raises a code smell that the request and exception params here
# are redundant, however, Django requires them
def oppia_403_handler(request, exception):
    return HttpResponseForbidden('403.html')
