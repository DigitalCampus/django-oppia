# oppia/profile/admin.py

from django.contrib import admin

from profile.models import UserProfile, CustomField, UserProfileCustomField


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'can_upload', 'about', 'job_title', 'organisation', 'phone_number')


class CustomFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'order', 'type', 'required')


class UserProfileCustomFieldAdmin(admin.ModelAdmin):
    list_display = ('key_name', 'user', 'value_str', 'value_int', 'value_bool')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CustomField, CustomFieldAdmin)
admin.site.register(UserProfileCustomField, UserProfileCustomFieldAdmin)
