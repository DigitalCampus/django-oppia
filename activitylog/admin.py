# oppia/activitylog/admin.py
from django.contrib import admin

from activitylog.models import UploadedActivityLog


class UploadedActivityLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_user', 'file', 'created_date')
    search_fields = ['create_user__username', 'file']


admin.site.register(UploadedActivityLog, UploadedActivityLogAdmin)
