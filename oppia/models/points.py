
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

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
        for idx, u in enumerate(users_points):
            user = User.objects.get(pk=u['user'])
            user.badges = 0 if u['badges'] is None else u['badges']
            user.total = 0 if u['points'] is None else u['points']
            leaderboard.append(user)

        return leaderboard

    @staticmethod
    def get_leaderboard_filtered(request_user,
                                 count_top=20,
                                 above=20,
                                 below=20):

        from summary.models import UserPointsSummary

        users_points = UserPointsSummary.objects.all() \
            .values('user', 'points', 'badges') \
            .order_by('-points')

        # check if there's going to be overlap or not
        print(users_points.count())
        if users_points.count() <= (count_top + above + below + 1):
            return Points.get_leaderboard_top(users_points,
                                              users_points.count())

        leaderboard_data = Points.get_leaderboard_top(users_points, count_top)
        leaderboard_data = \
            Points.get_leaderboard_around_user(leaderboard_data,
                                               users_points,
                                               request_user,
                                               count_top,
                                               above,
                                               below)

        return leaderboard_data

    @staticmethod
    def get_leaderboard_top(users_points, count_top):

        leaderboard_data = []
        top_users_points = users_points[:count_top]

        for idx, u in enumerate(top_users_points):
            user = User.objects.get(pk=u['user'])
            user.badges = 0 if u['badges'] is None else u['badges']
            user.total = 0 if u['points'] is None else u['points']

            leader_data = {}
            leader_data['position'] = idx + 1
            leader_data['username'] = user.username
            leader_data['first_name'] = user.first_name
            leader_data['last_name'] = user.last_name
            leader_data['points'] = user.total
            leader_data['badges'] = user.badges

            leaderboard_data.append(leader_data)

        return leaderboard_data

    @staticmethod
    def get_leaderboard_around_user(leaderboard_data,
                                    users_points,
                                    request_user,
                                    count_top,
                                    above,
                                    below):

        # find position of current user
        request_user_position = 0
        for idx, up in enumerate(users_points):
            if up['user'] == request_user.pk:
                request_user_position = idx + 1
                break

        if request_user_position == 0:
            return leaderboard_data

        start_pos = request_user_position - above
        end_pos = request_user_position + below + 1
        # negative start_pos not supported
        if start_pos < 0:
            start_pos = 0

        # if user is already in the top count_top + below, calculate correct
        # start and end pos
        if request_user_position <= count_top + below:
            start_pos = count_top
            end_pos = request_user_position + below

        user_above_below_points = users_points[start_pos:end_pos]

        for idx, u in enumerate(user_above_below_points):
            user = User.objects.get(pk=u['user'])
            user.badges = 0 if u['badges'] is None else u['badges']
            user.total = 0 if u['points'] is None else u['points']

            leader_data = {}
            leader_data['position'] = start_pos + idx + 1
            leader_data['username'] = user.username
            leader_data['first_name'] = user.first_name
            leader_data['last_name'] = user.last_name
            leader_data['points'] = user.total
            leader_data['badges'] = user.badges

            leaderboard_data.append(leader_data)

        return leaderboard_data

    @staticmethod
    def get_userscore(user):
        score = Points.objects.filter(user=user) \
            .aggregate(total=Sum('points'))
        if score['total'] is None:
            return 0
        return score['total']
