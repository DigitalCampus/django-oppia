# oppia/reports/admin.py

from django.contrib import admin

from oppia.reports.models import DashboardAccessLog

class DashboardAccessLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'access_date', 'url', 'ip')
    
admin.site.register(DashboardAccessLog, DashboardAccessLogAdmin)  