from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from profile.models import CustomField, UserProfileCustomField

from tests.user_logins import NORMAL_USER


class ProfileModelsTest(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json']
    VALUE_STR_DEFAULT = "my string"

    def setUp(self):
        super(ProfileModelsTest, self).setUp()
        self.user = User.objects.get(pk=NORMAL_USER['id'])

    # test get_value string
    def test_custom_field_get_value_str(self):
        custom_field = CustomField(
            id='str',
            label='String',
            required=True,
            type='str')
        custom_field.save()

        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_str=self.VALUE_STR_DEFAULT)
        upcf.save()

        self.assertEqual(upcf.get_value(), self.VALUE_STR_DEFAULT)
        self.assertNotEqual(upcf.get_value(), True)
        self.assertNotEqual(upcf.get_value(), False)
        self.assertNotEqual(upcf.get_value(), None)
        self.assertNotEqual(upcf.get_value(), 123)

    # test get_value int
    def test_custom_field_get_value_int(self):
        custom_field = CustomField(
            id='int',
            label='Integer',
            required=True,
            type='int')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_int=123)
        upcf.save()

        self.assertEqual(upcf.get_value(), 123)
        self.assertNotEqual(upcf.get_value(), "123")
        self.assertNotEqual(upcf.get_value(), True)
        self.assertNotEqual(upcf.get_value(), False)
        self.assertNotEqual(upcf.get_value(), None)

    # get get value bool
    def test_custom_field_get_value_bool(self):
        custom_field = CustomField(
            id='bool',
            label='Boolean',
            required=True,
            type='bool')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_bool=True)
        upcf.save()

        self.assertEqual(upcf.get_value(), True)
        self.assertNotEqual(upcf.get_value(), "True")
        self.assertNotEqual(upcf.get_value(), 123)
        self.assertNotEqual(upcf.get_value(), False)
        self.assertNotEqual(upcf.get_value(), None)

    # test multiple rows in userprofilecustomfield
    def test_custom_field_multiple_rows(self):
        custom_field = CustomField(
            id='str',
            label='String',
            required=True,
            type='str')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_str=self.VALUE_STR_DEFAULT)
        upcf.save()

        with self.assertRaises(IntegrityError):
            upcf = UserProfileCustomField(key_name=custom_field,
                                          user=self.user,
                                          value_str="my other string")
            upcf.save()

    def test_wrong_type_bool_in_int(self):
        custom_field = CustomField(
            id='int',
            label='Integer',
            required=True,
            type='int')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_int=True)
        upcf.save()

        self.assertEqual(True, upcf.get_value())
        upcf.value_int = False
        upcf.save()
        self.assertEqual(False, upcf.get_value())

    def test_wrong_type_bool_in_str(self):
        custom_field = CustomField(
            id='str',
            label='String',
            required=True,
            type='str')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_str=True)
        upcf.save()
        self.assertEqual(True, upcf.get_value())
        upcf.value_str = False
        upcf.save()
        self.assertEqual(False, upcf.get_value())

    def test_wrong_type_int_in_bool_123(self):
        custom_field = CustomField(
            id='bool',
            label='Boolean',
            required=True,
            type='bool')
        custom_field.save()
        with self.assertRaises(ValidationError):
            UserProfileCustomField(key_name=custom_field,
                                   user=self.user,
                                   value_bool=123).save()

    def test_wrong_type_int_in_bool_0(self):
        custom_field = CustomField(
            id='bool',
            label='Boolean',
            required=True,
            type='bool')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_bool=0)
        upcf.save()
        self.assertEqual(0, upcf.get_value())

    def test_wrong_type_int_in_bool_1(self):
        custom_field = CustomField(
            id='bool',
            label='Boolean',
            required=True,
            type='bool')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_bool=1)
        upcf.save()
        self.assertEqual(1, upcf.get_value())

    def test_wrong_type_int_in_str(self):
        custom_field = CustomField(
            id='str',
            label='String',
            required=True,
            type='str')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.user,
                                      value_str=123)
        upcf.save()
        self.assertEqual(123, upcf.get_value())

    def test_wrong_type_str_in_bool(self):
        custom_field = CustomField(
            id='bool',
            label='Boolean',
            required=True,
            type='bool')
        custom_field.save()
        with self.assertRaises(ValidationError):
            UserProfileCustomField(key_name=custom_field,
                                   user=self.user,
                                   value_bool=self.VALUE_STR_DEFAULT).save()

    def test_wrong_type_str_in_int(self):
        custom_field = CustomField(
            id='int',
            label='Integer',
            required=True,
            type='int')
        custom_field.save()
        with self.assertRaises(ValueError):
            UserProfileCustomField(key_name=custom_field,
                                   user=self.user,
                                   value_int=self.VALUE_STR_DEFAULT).save()
