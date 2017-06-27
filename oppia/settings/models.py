from django.db import models

class SettingProperties(models.Model):
    key = models.CharField(max_length=30, null=False, primary_key=True)
    str_value = models.CharField(max_length=50,blank=True, null=True)
    int_value = models.IntegerField()

    @staticmethod
    def get_property(propertyKey, defaultValue):
        try:
            prop = SettingProperties.objects.get(key=propertyKey)
            value = prop.str_value if prop.str_value is not None else prop.int_value
            if value is not None:
                return value

        except SettingProperties.DoesNotExist:
            pass

        return defaultValue