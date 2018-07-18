from django.contrib import admin

from settings.models import SettingProperties


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'str_value', 'int_value')

admin.site.register(SettingProperties, SettingsAdmin)
