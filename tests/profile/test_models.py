from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase

from profile.models import CustomField, UserProfileCustomField

from tests.user_logins import NORMAL_USER


class ProfileModelsTest(TestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json']

    def setUp(self):
        super(ProfileModelsTest, self).setUp()

    # test get_value string
    def test_custom_field_get_value_str(self):
        custom_field = CustomField(
            id='str',
            label='String',
            required=True,
            type='str')
        custom_field.save()
        user = User.objects.get(pk=NORMAL_USER['id'])
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=user,
                                      value_str="my string")
        upcf.save()

        self.assertEqual(upcf.get_value(), "my string")
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
        user = User.objects.get(pk=NORMAL_USER['id'])
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=user,
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
        user = User.objects.get(pk=NORMAL_USER['id'])
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=user,
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
        user = User.objects.get(pk=NORMAL_USER['id'])
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=user,
                                      value_str="my string")
        upcf.save()
        
        with self.assertRaises(IntegrityError):
            upcf = UserProfileCustomField(key_name=custom_field,
                                          user=user,
                                          value_str="my other string")
            upcf.save()