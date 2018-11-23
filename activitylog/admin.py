# oppia/activitylog/admin.py
from django.contrib import admin

from activitylog.models import UploadedActivityLog


class UploadedActivityLogAdmin(admin.ModelAdmin):
    list_display = ('file', 'created_date')

admin.site.register(UploadedActivityLog, UploadedActivityLogAdmin)
