
from django.conf import settings

from oppia import badges
from oppia.models import Badge, BadgeMethod, Course


def courses_completed(hours):
    try:
        badge = Badge.objects.get(ref='coursecompleted')
    except Badge.DoesNotExist:
        print("Badge not found: coursecompleted")
        return False

    courses = Course.objects.filter(is_draft=False, is_archived=False)
    
    for course in courses:
        print(course.get_title())
        print(badge.default_method)
        print(hours)
    
        if badge.default_method \
           == BadgeMethod.objects.get(key='all_activities'):
                badge_awarding = badges.BadgeAllActivities()
        elif badge.default_method \
           == BadgeMethod.objects.get(key='final_quiz'):
                badge_awarding = badges.BadgeFinalQuiz()
        elif badge.default_method \
           == BadgeMethod.objects.get(key='all_quizzes'):
                badge_awarding = badges.BadgeAllQuizzes()
        elif badge.default_method \
           == BadgeMethod.objects.get(key='all_quizzes_plus_percent'):
                badge_awarding = badges.BadgeAllQuizzesPlusPercent()
        else:
            return False # invalid badge method selected
        
        badge_awarding.process(course, badge, hours)
        
    return True
      