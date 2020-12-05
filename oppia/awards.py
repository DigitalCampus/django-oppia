
from django.conf import settings

from oppia import badges
from oppia.models import Badge, Course


def courses_completed(hours):
    try:
        badge = Badge.objects.get(ref='coursecompleted')
    except Badge.DoesNotExist:
        print("Badge not found: coursecompleted")
        return False

    courses = Course.objects.filter(is_draft=False, is_archived=False)
    
    for course in courses:
        print(course.get_title())
        print(settings.BADGE_AWARDING_METHOD)
        print(hours)
    
        if settings.BADGE_AWARDING_METHOD \
           == settings.BADGE_AWARD_METHOD_ALL_ACTIVITIES:
                badge_awarding = badges.BadgeAllActivities()
        elif settings.BADGE_AWARDING_METHOD \
            == settings.BADGE_AWARD_METHOD_FINAL_QUIZ:
                badge_awarding = badges.BadgeFinalQuiz()
        elif settings.BADGE_AWARDING_METHOD \
           == settings.BADGE_AWARD_METHOD_ALL_QUIZZES:
                badge_awarding = badges.BadgeAllQuizzes()
        elif settings.BADGE_AWARDING_METHOD \
           == settings.BADGE_AWARD_METHOD_QUIZZES_PLUS_PERCENT:
                badge_awarding = badges.BadgeAllQuizzesPlusPercent()
        else:
            return False # invalid badge method selected
        
        badge_awarding.process(course, badge, hours)
        
    return True
      