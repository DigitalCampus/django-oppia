from abc import abstractmethod

from django.db import models

from oppia.models import Award, AwardCourse
from oppia.signals import badgeaward_callback

models.signals.post_save.connect(badgeaward_callback, sender=Award)


class BaseBadge():

    STR_COURSE_COMPLETED = "Course completed: "

    @abstractmethod
    def process(self, course, badge, hours):
        pass

    def award_badge(self, course, user, badge):
        print(course.get_title())
        print("-----------------------------")
        print(user.username + " AWARD BADGE")
        award = Award()
        award.badge = badge
        award.user = user
        award.description = self.STR_COURSE_COMPLETED \
            + course.get_title()
        award.save()

        ac = AwardCourse()
        ac.course = course
        ac.award = award
        ac.course_version = course.version
        ac.save()
