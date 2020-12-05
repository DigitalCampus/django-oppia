import datetime

from django.contrib.auth.models import User
from django.utils import timezone

from oppia.badges.base_badge import BaseBadge
from oppia.models import Tracker, Course, Activity


class BadgeFinalQuiz(BaseBadge):

    def process(self, course, badge, hours):
        final_quiz_digest_activity = Activity \
            .objects \
            .filter(section__course=course, type=Activity.QUIZ) \
            .order_by('-section__order', '-order')[:1]

        if final_quiz_digest_activity.count() != 1:
            return
        final_quiz_digest = final_quiz_digest_activity[0].digest
        print(final_quiz_digest)
        print(course.get_title())

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
            user_completed = Tracker.objects \
                .filter(user=user,
                        course=course,
                        completed=True,
                        digest=final_quiz_digest) \
                .values('digest') \
                .distinct() \
                .count()
            if user_completed > 0:
                self.award_badge(course, user, badge)
