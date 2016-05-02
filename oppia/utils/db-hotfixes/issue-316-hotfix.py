'''
Script to fix database after users have been given badges multiple times for the same course

see: https://github.com/DigitalCampus/django-oppia/issues/316

'''

def run():

	from django.db.models import Q, Count, Min
	from django.contrib.auth.models import User
	from oppia.models import Course, Award, AwardCourse

	users = User.objects.filter(~Q(award = None)).distinct()

	for user in users:
		awards = Award.objects.filter(user=user)

		for award in awards:
			awardcourses = AwardCourse.objects.filter(award=award)
			for awardcourse in awardcourses:
				#print awardcourse.course
				duplicates = Award.objects.filter(user=user, awardcourse__course = awardcourse.course)
				if duplicates.count() > 1:
					print user,  "*** ", duplicates.count(), " ****"
					first_award = duplicates.aggregate(first=Min('award_date'))
					print first_award['first']
					Award.objects.filter(user=user, awardcourse__course = awardcourse.course).exclude(award_date = first_award['first']).delete()
		

if __name__ == "__main__":
    import django
    django.setup()
    run() 
