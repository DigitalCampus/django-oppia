# oppia/viz/admin.py
from django.contrib import admin
from oppia.viz.models import UserLocationVisualization


class UserLocationVisualizationAdmin(admin.ModelAdmin):
    list_display = ('ip', 'lat', 'lng', 'hits', 'region', 'country_name', 'country_code', )

admin.site.register(UserLocationVisualization, UserLocationVisualizationAdmin)
