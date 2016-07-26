from django.contrib import admin

from oppia.summary.models import UserCourseSummary, CourseDailyStats, SettingProperties




class UserCourseSummaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'points', 'total_downloads', 'total_activity', 'quizzes_passed',
                    'badges_achieved', 'pretest_score', 'media_viewed', 'completed_activities')
    actions = ['update_summary']

    def update_summary(self, request, queryset):
        for courseSummary in queryset:
            courseSummary.update_summary()

    update_summary.short_description = "Update summary"

class CourseDailyStatsAdmin(admin.ModelAdmin):
    list_display = ('course', 'day', 'type', 'total')


admin.site.register(UserCourseSummary, UserCourseSummaryAdmin)
admin.site.register(CourseDailyStats, CourseDailyStatsAdmin)
admin.site.register(SettingProperties)
