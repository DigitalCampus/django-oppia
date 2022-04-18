
from django.contrib import admin
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html

from oppia.models import Course, \
                         Section, \
                         Activity, \
                         Tracker, \
                         Media, \
                         Cohort, \
                         CoursePermissions
from oppia.models import Participant, Category, CourseCategory
from oppia.models import Badge, Award, Points, AwardCourse, BadgeMethod
from oppia.models import CourseCohort, CoursePublishingLog
from oppia.models import CertificateTemplate

from quiz.models import Question, QuizProps


class TrackerAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'submitted_date',
                    'tracker_date',
                    'time_taken',
                    'event',
                    'points',
                    'course',
                    'completed')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title_lang',
                    'shortname',
                    'version',
                    'lastupdated_date',
                    'user',
                    'filename',
                    'is_draft',
                    'is_archived',
                    'new_downloads_enabled')
    search_fields = ['title', 'shortname', 'version', 'filename']

    def title_lang(self, obj):
        return obj.get_title()


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('cohort', 'user', 'role')


class ParticipantInline(admin.TabularInline):
    model = Participant


class CohortAdmin(admin.ModelAdmin):
    list_display = ('description', 'start_date', 'end_date')
    inlines = [
        ParticipantInline,
    ]


class CourseCohortAdmin(admin.ModelAdmin):
    list_display = ('course', 'cohort')


class BadgeMethodAdmin(admin.ModelAdmin):
    list_display = ('key', 'description')


class BadgeAdmin(admin.ModelAdmin):
    list_display = ('description', 'points', 'default_method')


class PointsAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'course', 'points', 'date', 'description')


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title_lang', 'section', 'type', 'digest')
    search_fields = ['title', 'type', 'digest']

    def title_lang(self, obj):
        return obj.get_title()


class AwardCourseAdmin(admin.ModelAdmin):
    list_display = ('award', 'course', 'course_version')


class AwardAdmin(admin.ModelAdmin):
    list_display = ('badge', 'user', 'description', 'award_date')


class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('course', 'category')


class CoursePublishingLogAdmin(admin.ModelAdmin):
    list_display = ('course',
                    'new_version',
                    'old_version',
                    'user',
                    'action',
                    'data')


class CoursePermissionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'role')


class MediaAdmin(admin.ModelAdmin):
    list_display = ('course', 'digest', 'filename', 'download_url')


class SectionAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'order')
    search_fields = ['title']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'created_date',
                    'created_by',
                    'description',
                    'order_priority',
                    'highlight')
    ordering = ['-order_priority', 'name']
    search_fields = ['name', 'description']


class CertificateTemplateAdmin(admin.ModelAdmin):
    list_display = ('course',
                    'badge',
                    'enabled',
                    'display_name_method',
                    'include_name',
                    'include_date',
                    'include_course_title',
                    'validation',
                    'preview')

    def preview(self, obj):
        return format_html("<a target='_blank' href="
                           + reverse('oppia:certificate_preview',
                                     args={obj.id})
                           + ">Sample</a>")

    def get_form(self, request, obj=None, **kwargs):
        self.instance = obj
        return super(CertificateTemplateAdmin, self).get_form(
            request, obj=obj, **kwargs)

    # filter to only feedback questions
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'feedback_field':
            feedback_activities = Activity.objects.filter(
                type=Activity.FEEDBACK).values_list('digest', flat=True)
            quizzes = QuizProps.objects.filter(name='digest',
                                               value__in=feedback_activities) \
                .values_list('quiz_id',
                             flat=True)
            kwargs['queryset'] = Question.objects.filter(
                quizquestion__quiz__pk__in=quizzes).filter(
                (Q(type='essay') | Q(type='shortanswer')))
        return super(CertificateTemplateAdmin, self).formfield_for_foreignkey(
            db_field, request=request, **kwargs)

    preview.short_description = "Preview/Test"


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Award, AwardAdmin)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(BadgeMethod, BadgeMethodAdmin)
admin.site.register(AwardCourse, AwardCourseAdmin)
admin.site.register(Cohort, CohortAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseCohort, CourseCohortAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Points, PointsAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tracker, TrackerAdmin)
admin.site.register(CoursePermissions, CoursePermissionsAdmin)
admin.site.register(CoursePublishingLog, CoursePublishingLogAdmin)
admin.site.register(CertificateTemplate, CertificateTemplateAdmin)
