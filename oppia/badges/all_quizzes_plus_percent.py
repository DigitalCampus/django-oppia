import datetime

from django.contrib.auth.models import User
from django.utils import timezone

from oppia.badges.base_badge import BaseBadge
from oppia.models import Tracker, Course, Activity

from settings import constants
from settings.models import SettingProperties


class BadgeAllQuizzesPlusPercent(BaseBadge):

    def process(self, course, badge, hours):
        quiz_digests = Activity.objects.filter(section__course=course,
                                          type=Activity.QUIZ) \
            .values('digest') \
            .distinct()

        other_digests = Activity.objects \
            .filter(section__course=course).exclude(type=Activity.QUIZ) \
            .values('digest') \
            .distinct()

        # get all the users who've added tracker for this course in last
        # 'hours'
        if hours == 0:
            users = User.objects.filter(tracker__course=course)
        else:
            since = timezone.now() - datetime.timedelta(hours=int(hours))
            users = User.objects.filter(tracker__course=course,
                                        tracker__submitted_date__gte=since)

        # exclude the users that already own this course award
        users = users.exclude(award__awardcourse__course=course).distinct()

        for user in users:
            # check all quizzes have been completed
            user_completed_quizzes = Tracker.objects.filter(
                user=user,
                course=course,
                completed=True,
                type=Activity.QUIZ,
                digest__in=quiz_digests) \
                .values('digest') \
                .distinct() \
                .count()

            # check percentage of other activities completed
            user_completed_other = Tracker.objects.filter(
                user=user,
                course=course,
                completed=True,
                digest__in=other_digests) \
                .exclude(type=Activity.QUIZ) \
                .values('digest') \
                .distinct() \
                .count()

            percent_complete = (user_completed_other/
                                len(other_digests))*100

            if quiz_digests.count() == user_completed_quizzes and \
                percent_complete >= SettingProperties.get_property(
                    constants.OPPIA_BADGES_PERCENT_COMPLETED, 80):
                self.award_badge(course, user, badge)
