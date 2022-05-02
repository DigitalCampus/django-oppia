from dbview.models import DbView

from django.contrib.auth.models import User

class ViewUserCourseCompletePercent(DbView):
    
    @classmethod
    def view(cls):
        """
        exclude staff/admin users
        exclude user from reporting
        """
        qs = User.objects.all().values('username',
                                       'first_name',
                                       'last_name',
                                       'email',
                                       'userprofile__phone_number')
        return str(qs.query)