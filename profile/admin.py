# oppia/profile/admin.py

from django.contrib import admin

from profile.models import UserProfile, CustomField, UserProfileCustomField


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'can_upload',
                    'exclude_from_reporting',
                    'job_title',
                    'organisation',
                    'phone_number',
                    'created',
                    'modified')
    readonly_fields = ['user']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email', 'organisation']


class CustomFieldAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'label',
                    'order',
                    'type',
                    'required',
                    'created',
                    'modified')


class UserProfileCustomFieldAdmin(admin.ModelAdmin):
    list_display = ('key_name',
                    'user',
                    'value_str',
                    'value_int',
                    'value_bool',
                    'created',
                    'modified')
    readonly_fields = ['user','key_name']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CustomField, CustomFieldAdmin)
admin.site.register(UserProfileCustomField, UserProfileCustomFieldAdmin)
