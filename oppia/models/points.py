
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from oppia.models import Course


class Points(models.Model):
    POINT_TYPES = (
        ('signup', 'Sign up'),
        ('userquizattempt', 'Quiz attempt by user'),
        ('firstattempt', 'First quiz attempt'),
        ('firstattemptscore', 'First attempt score'),
        ('firstattemptbonus', 'Bonus for first attempt score'),
        ('quizattempt', 'Quiz attempt'),
        ('quizcreated', 'Created quiz'),
        ('activitycompleted', 'Activity completed'),
        ('mediaplayed', 'Media played'),
        ('badgeawarded', 'Badge awarded'),
        ('coursedownloaded', 'Course downloaded'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course,
                               null=True,
                               default=None,
                               on_delete=models.SET_NULL)
    points = models.IntegerField()
    date = models.DateTimeField('date created', default=timezone.now)
    description = models.TextField(blank=False)
    data = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=POINT_TYPES)

    class Meta:
        verbose_name = _('Points')
        verbose_name_plural = _('Points')

    def __str__(self):
        return self.description

    @staticmethod
    def get_leaderboard(count=0, course=None):

        from summary.models import UserCourseSummary, UserPointsSummary

        if course is not None:
            users = UserCourseSummary.objects.filter(course=course)
            users_points = users.values('user') \
                .annotate(points=Sum('points'),
                          badges=Sum('badges_achieved')) \
                .order_by('-points')
        else:
            users_points = UserPointsSummary.objects.all() \
                .values('user', 'points', 'badges') \
                .order_by('-points')

        if count > 0:
            users_points = users_points[:count]

        leaderboard = []
        for u in users_points:
            user = User.objects.get(pk=u['user'])
            user.badges = 0 if u['badges'] is None else u['badges']
            user.total = 0 if u['points'] is None else u['points']
            leaderboard.append(user)

        return leaderboard

    @staticmethod
    def get_userscore(user):
        score = Points.objects.filter(user=user) \
            .aggregate(total=Sum('points'))
        if score['total'] is None:
            return 0
        return score['total']
