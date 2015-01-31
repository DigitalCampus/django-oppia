# oppia/awards.py
from django.db import models
from django.db.models import Count, F
from django.contrib.auth.models import User

from oppia.models import Badge, Award, AwardCourse
from oppia.models import Tracker, Course, Section, Activity, Media
from oppia.quiz.models import Quiz, QuizAttempt, QuizProps
from oppia.signals import badgeaward_callback

models.signals.post_save.connect(badgeaward_callback, sender=Award)

def courses_completed(hours):
    try:
        badge = Badge.objects.get(ref='coursecompleted')
    except Badge.DoesNotExist:
        print "Badge not found: coursecompleted"
        return
    
    print hours
    # create batch of course with all the digests for each course
    courses = Course.objects.filter(is_draft=False, is_archived=False)
    for c in courses:
        digests = Activity.objects.filter(section__course=c).values('digest').distinct()
        print c.title
        print "-----------------------------"
        print digests.count()
        print "\n\n"
    
    # create set of users to     
    exit()
    
    
    
    
    
    
    users = Tracker.objects.values('user_id').distinct()
    courses = Course.objects.all()
    for u in users:
        user = User.objects.get(pk=u['user_id'])
        #loop through the courses
        for c in courses:
            # check if the user has already been awarded for this course
            already_completed = AwardCourse.objects.filter(award__user=user,course=c) 
            if already_completed.count() == 0:
                if media_complete(user,c) and activities_complete(user,c) and quiz_complete(user,c):
                    print "%s badge awarded to %s" % (badge, user.username)
                    award = Award()
                    award.badge = badge
                    award.user = user
                    award.description = "Course completed: " + c.get_title()
                    award.save()
                    
                    am = AwardCourse()
                    am.course = c
                    am.award = award
                    am.course_version = c.version
                    am.save()
    return

def activities_complete(user,course):
    digests = Activity.objects.filter(section__course=course).values('digest').distinct()
    user_completed = Tracker.objects.filter(user=user,completed=True,digest__in=digests).values('digest').distinct()
    if digests.count() == user_completed.count():
        print user.first_name + " completed activities in " + course.get_title()
        return True
    else:
        return False 
    
def media_complete(user,course):
    digests = Media.objects.filter(course=course).values('digest').distinct()
    if digests.count() == 0:
        return True
    user_completed = Tracker.objects.filter(user=user,completed=True,digest__in=digests).values('digest').distinct()
    if digests.count() == user_completed.count():
        print user.first_name + " completed media in " + course.get_title()
        return True
    else:
        return False 
    
def quiz_complete(user,course):
    digests = Activity.objects.filter(section__course=course, type='quiz',baseline=False).values('digest').distinct()
    if digests.count() == 0:
        return True
    quizzes = QuizProps.objects.filter(name='digest', value__in=digests).values('quiz_id').distinct()
    #quiz_attempts = QuizAttempt.objects.filter(user=user,quiz__in=quizzes,score=F('maxscore')).values('quiz_id').distinct()
    # TODO - sure this could be done better...
    quiz_attempts = QuizAttempt.objects.filter(user=user,quiz__in=quizzes)
    results = []
    for qa in quiz_attempts:
        if qa.get_score_percent() == 100:
            try:
                results.index(qa.quiz_id)
            except ValueError:
                results.append(qa.quiz_id)          
    if quizzes.count() == len(results):
        print user.first_name + " completed quizzes in " + course.get_title()
        return True
    else: 
        return False