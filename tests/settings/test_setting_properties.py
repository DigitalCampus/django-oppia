
from django.test import TestCase
from settings.models import SettingProperties

class SettingPropertiesTest(TestCase):
    
    
    def test_self_name_int(self):
        sp = SettingProperties()
        sp.key = u"testintkey"
        sp.int_value = 123
        sp.save()
        self.assertEqual(sp.__unicode__(), u"testintkey")
    
    def test_self_name_string(self):
        sp = SettingProperties()
        sp.key = u"teststrkey"
        sp.str_value = u"test string"
        sp.save()
        self.assertEqual(sp.__unicode__(), u"teststrkey")
        
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
        self.assertEqual(value, retreived_value)
        
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
        
    def test_string_is_null(self):
        key = "intkey"
        value = 123
        SettingProperties.set_int(key, value)
        retreived_value = SettingProperties.get_string(key, "default")
        self.assertEqual("default", retreived_value)
        
    def test_int_is_null(self):
        key = "testkey"
        value = "testval"
        SettingProperties.set_string(key, value)
        retreived_value = SettingProperties.get_int(key, 123)
        self.assertEqual(123, retreived_value)
        
    def test_get_prop_string(self):
        key = "testkey"
        value = "testval"
        SettingProperties.set_string(key, value)
        retreived_value = SettingProperties.get_property(key, "default")
        self.assertEqual(value, retreived_value)
        
    def test_get_prop_int(self):
        key = "testkey"
        value = 123
        SettingProperties.set_int(key, value)
        retreived_value = SettingProperties.get_property(key, 0)
        self.assertEqual(value, retreived_value)
     
    def test_get_prop_string_none(self):
        key = "testkey"
        value = None
        SettingProperties.set_string(key, value)
        retreived_value = SettingProperties.get_property(key, "default")
        self.assertEqual("default", retreived_value)  
        
    def test_get_prop_int_none(self):
        key = "testkey"
        value = None
        SettingProperties.set_int(key, value)
        retreived_value = SettingProperties.get_property(key, 100)
        self.assertEqual(100, retreived_value) 
        
    def test_get_prop_int_doesnotexist(self):
        key = "testkey"
        value = 123
        SettingProperties.set_int(key, value)
        retreived_value = SettingProperties.get_property("some non key", 100)
        self.assertEqual(100, retreived_value)
        
    def test_get_prop_string_doesnotexist(self):
        key = "testkey"
        value = "mystring"
        SettingProperties.set_string(key, value)
        retreived_value = SettingProperties.get_property("some non key", "not here")
        self.assertEqual("not here", retreived_value)
        