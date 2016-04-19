# oppia/profile/admin.py

from django.contrib import admin

from oppia.profile.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'can_upload', 'about', 'job_title', 'organisation')

admin.site.register(UserProfile, UserProfileAdmin)