from django.db.models import Count, F

from dbview.models import DbView

from profile.models import UserProfileCustomField


class ViewUserCourseCompletePercent(DbView):

    @classmethod
    def view(cls):
        qs = UserProfileCustomField.objects.filter(
            user__is_staff=False,
            user__is_superuser=False,
            user__userprofile__exclude_from_reporting=False) \
            .values('id',
                    userid=F('user__id'),
                    username=F('user__username'),
                    first_name=F('user__first_name'),
                    last_name=F('user__last_name'),
                    email=F('user__email'),
                    phone_number=F('user__userprofile__phone_number'),
                    profile_field_name=F('key_name'),
                    profile_field_value_int=F('value_int'),
                    profile_field_value_str=F('value_str'),
                    profile_field_value_bool=F('value_bool'),
                    course_id=F('user__usercoursesummary__course__id'),
                    course_title=F('user__usercoursesummary__course__title'),
                    no_activities_completed=F('user__usercoursesummary__completed_activities')) \
            .annotate(
                total_no_activities=Count(
                    'user__usercoursesummary__course__section__activity')) \
            .annotate(
                percent_complete=F(
                    'no_activities_completed') / F(
                    'total_no_activities') * 100)

        return str(qs.query)
