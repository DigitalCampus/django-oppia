# oppia/gamification/admin.py
from django.contrib import admin

from gamification.models import CourseGamificationEvent, \
                                ActivityGamificationEvent, \
                                MediaGamificationEvent, \
                                DefaultGamificationEvent


class CourseGamificationEventAdmin(admin.ModelAdmin):
    list_display = ('course', 'event', 'points')


class ActivityGamificationEventAdmin(admin.ModelAdmin):
    list_display = ('activity', 'event', 'points')


class MediaGamificationEventAdmin(admin.ModelAdmin):
    list_display = ('media', 'event', 'points')


class DefaultGamificationEventAdmin(admin.ModelAdmin):
    list_display = ('event', 'points', 'level')


admin.site.register(CourseGamificationEvent, CourseGamificationEventAdmin)
admin.site.register(ActivityGamificationEvent, ActivityGamificationEventAdmin)
admin.site.register(MediaGamificationEvent, MediaGamificationEventAdmin)
admin.site.register(DefaultGamificationEvent, DefaultGamificationEventAdmin)
