# oppia/permissions.py

from itertools import chain

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseForbidden

from oppia.models import Course, Participant, Cohort, CoursePermissions
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
    if request.user.is_staff:
        return True
    else:
        return False


def get_user(request, view_user_id):
    if request.user.is_staff or (request.user.id == int(view_user_id)):
        try:
            view_user = User.objects.get(pk=view_user_id)
            return view_user
        except User.DoesNotExist:
            raise Http404()
    try:
        view_user = User.objects.get(pk=view_user_id)
        courses = Course.objects.filter(
            coursecohort__cohort__participant__user=view_user,
            coursecohort__cohort__participant__role=Participant.STUDENT) \
            .filter(
                coursecohort__cohort__participant__user=request.user,
                coursecohort__cohort__participant__role=Participant.TEACHER) \
            .count()
        if courses > 0:
            return view_user
        else:
            raise PermissionDenied
    except User.DoesNotExist:
        raise PermissionDenied


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
        courses = Course.objects.filter(user=user).count()
        if courses > 0:
            return True

        courses = Course.objects.filter(
            coursepermissions__user=user,
            coursepermissions__role=CoursePermissions.MANAGER).count()
        if courses > 0:
            return True
    return False


def can_add_cohort(request):
    if request.user.is_staff:
        return True
    return False


def can_edit_cohort(request, cohort_id):
    if request.user.is_staff:
        return True
    return False


def can_view_cohort(request, cohort_id):
    try:
        cohort = Cohort.objects.get(pk=cohort_id)
    except Cohort.DoesNotExist:
        raise Http404

    try:
        if request.user.is_staff:
            return cohort
        return Cohort.objects.get(pk=cohort_id,
                                  participant__user=request.user,
                                  participant__role=Participant.TEACHER)
    except Cohort.DoesNotExist:
        raise PermissionDenied


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


def can_view_course(request, course_id):
    try:
        if request.user.is_staff:
            course = Course.objects.get(pk=course_id, is_archived=False)
        else:
            try:
                course = Course.objects.get(pk=course_id,
                                            is_draft=False,
                                            is_archived=False)
            except Course.DoesNotExist:
                course = Course.objects.get(
                    pk=course_id,
                    is_archived=False,
                    coursepermissions__course__id=course_id,
                    coursepermissions__user__id=request.user.id,
                    coursepermissions__role=CoursePermissions.VIEWER)
    except Course.DoesNotExist:
        raise Http404
    return course


def can_view_course_detail(request, course_id):
    if request.user.is_staff:
        try:
            course = Course.objects.get(pk=course_id)
            return course
        except Course.DoesNotExist:
            raise Http404
    else:
        try:
            course = Course.objects.get(
                        pk=course_id,
                        coursepermissions__course__id=course_id,
                        coursepermissions__user=request.user,
                        coursepermissions__role=CoursePermissions.MANAGER)
            return course
        except Course.DoesNotExist:
            raise PermissionDenied


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
        if manager_courses.count() > 0:
            return manager_courses

        courses = Course.objects.filter(is_draft=False,
                                        is_archived=False).order_by(order_by)
    return courses


def oppia_403_handler(request, exception):
    return HttpResponseForbidden('403.html')
