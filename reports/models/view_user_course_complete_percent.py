from django.db import models
from django.db.models import Count, F

from dbview.models import DbView

from profile.models import UserProfileCustomField
from summary.models import UserCourseSummary


class ViewUserCourseCompletePercent(DbView):

    @classmethod
    def view(cls):
        qs = UserProfileCustomField.objects.filter(
            user__is_staff=False,
            user__is_superuser=False,
            user__userprofile__exclude_from_reporting=False) \
            .values('id',
                    'user__id',
                    'user__username',
                    'user__first_name',
                    'user__last_name',
                    'user__email',
                    'user__userprofile__phone_number',
                    'key_name',
                    'value_int',
                    'value_str',
                    'value_bool',
                    'user__usercoursesummary__course__id',
                    'user__usercoursesummary__course__title',
                    'user__usercoursesummary__completed_activities') \
            .annotate(
                no_activities=Count(
                    'user__usercoursesummary__course__section__activity')) \
            .annotate(
                percent_complete=F(
                    'user__usercoursesummary__completed_activities') / F(
                    'no_activities') * 100)

        return str(qs.query)
        
