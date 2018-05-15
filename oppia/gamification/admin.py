# oppia/gamification/admin.py
from django.contrib import admin

from oppia.gamification.models import *

class CourseGamificationPointsAdmin(admin.ModelAdmin):
    list_display = ('course','points_type','points')

class ActivityGamificationPointsAdmin(admin.ModelAdmin):
    list_display = ('activity','points_type','points')
    
class MediaGamificationPointsAdmin(admin.ModelAdmin):
    list_display = ('media','points_type','points')
    
class QuizGamificationPointsAdmin(admin.ModelAdmin):
    list_display = ('quiz','points_type','points')   
   
admin.site.register(CourseGamificationPoints, CourseGamificationPointsAdmin)  
admin.site.register(ActivityGamificationPoints, ActivityGamificationPointsAdmin) 
admin.site.register(MediaGamificationPoints, MediaGamificationPointsAdmin) 
admin.site.register(QuizGamificationPoints, QuizGamificationPointsAdmin) 