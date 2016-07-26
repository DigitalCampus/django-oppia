from django.contrib import admin

from oppia.summary.models import UserCourseSummary, CourseDailyStats, SettingProperties


def message_user(model, request, model_name, query_count):
    if query_count == 1:
         model.message_user(request, model_name + " summary succesfully updated.")
    elif query_count > 0:
        model.message_user(request, model_name + " summaries succesfully updated.")

class UserCourseSummaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'points', 'total_downloads', 'total_activity', 'quizzes_passed',
                    'badges_achieved', 'pretest_score', 'media_viewed', 'completed_activities')
    actions = ['update_summary']

    def update_summary(self, request, queryset):
        for courseSummary in queryset:
            courseSummary.update_summary()
        message_user(self, request, "User-course", queryset.count())

    update_summary.short_description = "Update summary"

class CourseDailyStatsAdmin(admin.ModelAdmin):
    list_display = ('course', 'day', 'type', 'total')

    actions = ['update_summary']

    def update_summary(self, request, queryset):
        for dailyStats in queryset:
            CourseDailyStats.update_daily_summary(dailyStats.course.id, dailyStats.day)
        message_user(self, request, "Daily stats", queryset.count())

    update_summary.short_description = "Update summary"


admin.site.register(UserCourseSummary, UserCourseSummaryAdmin)
admin.site.register(CourseDailyStats, CourseDailyStatsAdmin)
admin.site.register(SettingProperties)
