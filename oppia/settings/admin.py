from oppia.settings.models import SettingProperties
from django.contrib import admin


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'str_value', 'int_value')

admin.site.register(SettingProperties, SettingsAdmin)
