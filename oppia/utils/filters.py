
from django.db.models import Q

from oppia.models import CourseStatus


class CourseFilter:
    IS_LIVE = Q(status__name=CourseStatus.LIVE)
    IS_NOT_LIVE = ~Q(status__name=CourseStatus.LIVE)
    IS_ARCHIVED = Q(status__name=CourseStatus.ARCHIVED)
    IS_NOT_ARCHIVED = ~Q(status__name=CourseStatus.ARCHIVED)
    IS_DRAFT = Q(status__name=CourseStatus.DRAFT)
    IS_NOT_DRAFT = ~Q(status__name=CourseStatus.DRAFT)
    NEW_DOWNLOADS_DISABLED = Q(status__name=CourseStatus.NEW_DOWNLOADS_DISABLED)
    NEW_DOWNLOADS_ENABLED = ~Q(status__name=CourseStatus.NEW_DOWNLOADS_DISABLED)
    IS_READ_ONLY = Q(status__name=CourseStatus.READ_ONLY)
    IS_NOT_READ_ONLY = ~Q(status__name=CourseStatus.READ_ONLY)


class CourseCategoryFilter:
    COURSE_IS_ARCHIVED = Q(coursecategory__course__status__name=CourseStatus.ARCHIVED)
    COURSE_IS_NOT_ARCHIVED = ~Q(coursecategory__course__status__name=CourseStatus.ARCHIVED)
    COURSE_IS_DRAFT = Q(coursecategory__course__status__name=CourseStatus.DRAFT)
    COURSE_IS_NOT_DRAFT = ~Q(coursecategory__course__status__name=CourseStatus.DRAFT)
    COURSE_NEW_DOWNLOADS_DISABLED = Q(coursecategory__course__status__name=CourseStatus.NEW_DOWNLOADS_DISABLED)
    COURSE_NEW_DOWNLOADS_ENABLED = ~Q(coursecategory__course__status__name=CourseStatus.NEW_DOWNLOADS_DISABLED)
    COURSE_IS_READ_ONLY = Q(coursecategory__course__status__name=CourseStatus.READ_ONLY)
    COURSE_IS_NOT_READ_ONLY = ~Q(coursecategory__course__status__name=CourseStatus.READ_ONLY)
