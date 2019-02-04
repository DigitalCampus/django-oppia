
from django.test import TestCase
from settings.models import SettingProperties

class SettingPropertiesTest(TestCase):
    
    def test_set_string(self):
        key = "testkey"
        value = "testval"
        SettingProperties.set_string(key, value)
        retreived_value = SettingProperties.get_string(key, "default")
        self.assertEqual(value,retreived_value)
        
    def test_set_string_default(self):
        key = "testkey1"
        retreived_value = SettingProperties.get_string(key, "default")
        self.assertEqual("default", retreived_value)
        
    def test_set_int(self):
        key = "intkey"
        value = 123
        SettingProperties.set_int(key, value)
        retreived_value = SettingProperties.get_int(key, 0)
        self.assertEqual(value,retreived_value)
        
    def test_set_int_default(self):
        key = "testkey1"
        retreived_value = SettingProperties.get_int(key, 0)
        self.assertEqual(0, retreived_value)
        
    def test_delete_int(self):
        key = "testkey1"
        value = 123
        SettingProperties.set_int(key, value)
        SettingProperties.delete_key(key)
        retreived_value = SettingProperties.get_int(key, 0)
        self.assertEqual(0, retreived_value)
        
    def test_delete_string(self):
        key = "testkey1"
        value = "testval"
        SettingProperties.set_string(key, value)
        SettingProperties.delete_key(key)
        retreived_value = SettingProperties.get_string(key, "default")
        self.assertEqual("default", retreived_value)
        