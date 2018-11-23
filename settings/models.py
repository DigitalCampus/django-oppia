from django.db import models
from django.utils.translation import ugettext_lazy as _


class SettingProperties(models.Model):
    key = models.CharField(max_length=30, null=False, primary_key=True)
    str_value = models.CharField(max_length=50, blank=True, null=True)
    int_value = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = _('Settings')
        verbose_name_plural = _('Settings')
        ordering = ['key']

    @staticmethod
    def get_property(property_key, default_value):
        try:
            prop = SettingProperties.objects.get(key=property_key)
            value = prop.str_value if prop.str_value is not None else prop.int_value
            if value is not None:
                return value

        except SettingProperties.DoesNotExist:
            pass

        return default_value

    @staticmethod
    def get_int(property_key, default_value):
        try:
            prop = SettingProperties.objects.get(key=property_key)
            if prop.int_value is not None:
                return prop.int_value
        except SettingProperties.DoesNotExist:
            pass
        return default_value

    @staticmethod
    def get_string(property_key, default_value):
        try:
            prop = SettingProperties.objects.get(key=property_key)
            if prop.str_value is not None:
                return prop.str_value
        except SettingProperties.DoesNotExist:
            pass
        return default_value

    def __unicode__(self):
        return self.key
