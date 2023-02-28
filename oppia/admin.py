from django import forms
from django.contrib import admin, messages
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from oppia.models import Course, \
    Section, \
    Activity, \
    Tracker, \
    Media, \
    Cohort, \
    CoursePermissions, \
    CourseStatus, CohortCritera
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
                    'status')
    search_fields = ['title', 'shortname', 'version', 'filename']

    def title_lang(self, obj):
        return obj.get_title()

    def get_form(self, request, obj=None, **kwargs):
        form = super(CourseAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['status'].widget = forms.Select(
            choices=CourseStatus.get_available_statuses()
        )
        return form


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('cohort', 'user', 'role')


class CohortAdmin(admin.ModelAdmin):
    list_display = ('description', 'last_updated', 'criteria_based')
    actions = ['update_cohort', 'refresh_cohort']

    def success_message(self, request, intro, students, teachers):
        message = _("{} students and {} teachers match the criteria").format(students, teachers)
        message = intro + " " + message
        self.message_user(request, message=message)

    def error_message(self, request, cohort):
        self.message_user(request,
                          "Cohort '{}' is not criteria based.".format(cohort.description),
                          level=messages.ERROR)

    def update_cohort(self, request, queryset):
        for cohort in queryset:
            if not cohort.criteria_based:
                self.error_message(request, cohort)
                continue

            students, teachers = cohort.update_participants()
            cohort_title = _("Cohort '{}' updated successfully:").format(cohort.description)
            self.success_message(request, cohort_title, students, teachers)

    def refresh_cohort(self, request, queryset):
        for cohort in queryset:
            if not cohort.criteria_based:
                self.error_message(request, cohort)
                continue

            students, teachers = cohort.refresh_participants()
            cohort_title = _("Cohort '{}' refreshed successfully:").format(cohort.description)
            self.success_message(request, cohort_title, students, teachers)

    update_cohort.short_description = _('Update cohort participants')
    refresh_cohort.short_description = _('Refresh cohort participants')


class CohortCriteriaAdmin(admin.ModelAdmin):
    list_display = ('cohort', 'role', 'user_profile_field', 'user_profile_value')


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
            quizzes = QuizProps.objects.filter(name=QuizProps.DIGEST,
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
admin.site.register(CohortCritera, CohortCriteriaAdmin)
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
