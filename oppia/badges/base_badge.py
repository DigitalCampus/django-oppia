from abc import abstractmethod

from django.db import models

from oppia.models import Tracker, Course, Activity
from oppia.models import Badge, Award, AwardCourse
from oppia.signals import badgeaward_callback

models.signals.post_save.connect(badgeaward_callback, sender=Award)

class BaseBadge():
    
    STR_COURSE_COMPLETED = "Course completed: "
    
    @abstractmethod
    def process(self, badge, hours):
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

        am = AwardCourse()
        am.course = course
        am.award = award
        am.course_version = course.version
        am.save()