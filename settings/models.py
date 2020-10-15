from django.db import models
from django.utils.translation import ugettext_lazy as _


class SettingProperties(models.Model):
    key = models.CharField(max_length=50, null=False, primary_key=True)
    description = models.TextField(blank=True, null=True)
    str_value = models.CharField(max_length=200, blank=True, null=True)
    int_value = models.IntegerField(blank=True, null=True)
    bool_value = models.BooleanField(blank=True, null=True)

    class Meta:
        verbose_name = _('Settings')
        verbose_name_plural = _('Settings')
        ordering = ['key']

    @staticmethod
    def get_property(property_key, default_value):
        try:
            prop = SettingProperties.objects.get(key=property_key)
            value = None
            if prop.str_value is not None:
                value = prop.str_value
            elif prop.int_value is not None:
                value = prop.int_value
            elif prop.bool_value is not None:
                value = prop.bool_value
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

    @staticmethod
    def get_bool(property_key, default_value):
        try:
            prop = SettingProperties.objects.get(key=property_key)
            if prop.bool_value is not None:
                return prop.bool_value
        except SettingProperties.DoesNotExist:
            pass
        return default_value

    @staticmethod
    def set_int(property_key, value):
        prop, created = SettingProperties.objects \
            .get_or_create(key=property_key)
        prop.int_value = value
        prop.save()

    @staticmethod
    def set_string(property_key, value):
        prop, created = SettingProperties.objects \
            .get_or_create(key=property_key)
        prop.str_value = value
        prop.save()

    @staticmethod
    def set_bool(property_key, value):
        prop, created = SettingProperties.objects \
            .get_or_create(key=property_key)
        prop.bool_value = value
        prop.save()

    @staticmethod
    def delete_key(property_key):
        SettingProperties.objects.get(key=property_key).delete()

    def __str__(self):
        return self.key
