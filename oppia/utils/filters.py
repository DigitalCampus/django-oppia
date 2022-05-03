
from django.db.models import Q

from oppia.models import CourseStatus


class CourseFilter:
    IS_ARCHIVED = Q(status=CourseStatus.ARCHIVED)
    IS_NOT_ARCHIVED = ~Q(status=CourseStatus.ARCHIVED)
    IS_DRAFT = Q(status=CourseStatus.DRAFT)
    IS_NOT_DRAFT = ~Q(status=CourseStatus.DRAFT)
    NEW_DOWNLOADS_DISABLED = Q(status=CourseStatus.NEW_DOWNLOADS_DISABLED)
    NEW_DOWNLOADS_ENABLED = ~Q(status=CourseStatus.NEW_DOWNLOADS_DISABLED)


class CourseCategoryFilter:
    COURSE_IS_ARCHIVED = Q(coursecategory__course__status=CourseStatus.ARCHIVED)
    COURSE_IS_NOT_ARCHIVED = ~Q(coursecategory__course__status=CourseStatus.ARCHIVED)
    COURSE_IS_DRAFT = Q(coursecategory__course__status=CourseStatus.DRAFT)
    COURSE_IS_NOT_DRAFT = ~Q(coursecategory__course__status=CourseStatus.DRAFT)
    COURSE_NEW_DOWNLOADS_DISABLED = Q(coursecategory__course__status=CourseStatus.NEW_DOWNLOADS_DISABLED)
    COURSE_NEW_DOWNLOADS_ENABLED = ~Q(coursecategory__course__status=CourseStatus.NEW_DOWNLOADS_DISABLED)
