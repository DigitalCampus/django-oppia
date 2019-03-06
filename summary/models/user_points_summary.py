
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from oppia.models import Points
from summary.models.user_course_summary import UserCourseSummary

class UserPointsSummary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(blank=False, null=False, default=0)
    badges = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        verbose_name = _('UserPointsSummary')

    def update_points(self, last_points_pk=0, newest_points_pk=0):  # range of points ids to process

        first_points = (last_points_pk == 0)
        filters = {
            'pk__gt': last_points_pk,
            'user': self.user
        }
        if newest_points_pk > 0:
            filters['pk__lte'] = newest_points_pk

        new_points = Points.objects.filter( ** filters).aggregate(total=Sum('points'))['total']

        if not new_points:
            return

        # If we update the user points, we need to recalculate his badges as well
        badges = UserCourseSummary.objects.filter(user=self.user).aggregate(badges=Sum('badges_achieved'))['badges']
        self.badges = badges if badges else 0
        self.points = (0 if first_points else self.points) + new_points

        self.save()