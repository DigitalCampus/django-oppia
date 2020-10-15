from django.contrib import admin

from settings.models import SettingProperties


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('key',
                    'description',
                    'str_value',
                    'int_value',
                    'bool_value')


admin.site.register(SettingProperties, SettingsAdmin)
