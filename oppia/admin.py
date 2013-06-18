# oppia/admin.py
from oppia.models import *
from django.contrib import admin

class TrackerAdmin(admin.ModelAdmin):
    list_display = ('user', 'submitted_date', 'agent', 'course','completed')
    
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'version', 'lastupdated_date', 'user', 'filename')

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('cohort', 'user', 'role')
   
class CohortAdmin(admin.ModelAdmin):
    list_display = ('course', 'description', 'start_date', 'end_date')
    
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('description','points')
 
class PointsAdmin(admin.ModelAdmin):
    list_display = ('user','type','course','cohort','points','date','description')
     
admin.site.register(Course,CourseAdmin)
admin.site.register(Section)
admin.site.register(Activity)
admin.site.register(Tracker, TrackerAdmin)
admin.site.register(Media)
admin.site.register(Cohort, CohortAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Message)
admin.site.register(Schedule)
admin.site.register(ActivitySchedule)
admin.site.register(Tag)
admin.site.register(CourseTag)
admin.site.register(Badge,BadgeAdmin)
admin.site.register(Award)
admin.site.register(Points,PointsAdmin)
admin.site.register(AwardCourse)
admin.site.register(CourseDownload)
