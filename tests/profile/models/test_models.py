from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from oppia.test import OppiaTestCase

from profile.models import UserProfile, CustomField, UserProfileCustomField


class ProfileCustomFieldsTest(OppiaTestCase):
    fixtures = ['tests/test_user.json',
                'tests/test_oppia.json',
                'tests/test_quiz.json',
                'tests/test_course_permissions.json']
    VALUE_STR_DEFAULT = "my string"

    def test_custom_field_model_name(self):
        custom_field = CustomField(
            id='my_cf_key',
            label='String',
            required=True,
            type='str')
        custom_field.save()
        self.assertEqual(str(custom_field), 'my_cf_key')

    def test_teacher_only(self):
        user = self.normal_user
        self.assertFalse(user.userprofile.is_teacher_only())

    '''
    Upload permissions
    '''
    def test_get_can_upload_admin(self):
        profile = UserProfile.objects.get(user=self.admin_user)
        self.assertEqual(profile.get_can_upload(), True)

    def test_get_can_upload_staff(self):
        profile = UserProfile.objects.get(user=self.staff_user)
        self.assertEqual(profile.get_can_upload(), True)

    def test_get_can_upload_teacher(self):
        profile = UserProfile.objects.get(user=self.teacher_user)
        self.assertEqual(profile.get_can_upload(), True)

    def test_get_can_upload_user(self):
        profile = UserProfile.objects.get(user=self.normal_user)
        self.assertEqual(profile.get_can_upload(), False)

    def test_get_can_upload_activity_log_admin(self):
        profile = UserProfile.objects.get(user=self.admin_user)
        self.assertEqual(profile.get_can_upload_activitylog(), True)

    def test_get_can_upload_activity_log_staff(self):
        profile = UserProfile.objects.get(user=self.staff_user)
        self.assertEqual(profile.get_can_upload_activitylog(), True)

    def test_get_can_upload_activity_log_teacher(self):
        profile = UserProfile.objects.get(user=self.teacher_user)
        self.assertEqual(profile.get_can_upload_activitylog(), False)

    def test_get_can_upload_activity_log_user(self):
        profile = UserProfile.objects.get(user=self.normal_user)
        self.assertEqual(profile.get_can_upload_activitylog(), False)

    '''
    Custom fields
    '''
    def test_user_custom_field_model_name(self):
        custom_field = CustomField(
            id='str',
            label='String',
            required=True,
            type='str')
        custom_field.save()

        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.normal_user,
                                      value_str=self.VALUE_STR_DEFAULT)
        upcf.save()
        self.assertEqual('str: demo', str(upcf))

    # test get_value string
    def test_custom_field_get_value_str(self):
        custom_field = CustomField(
            id='str',
            label='String',
            required=True,
            type='str')
        custom_field.save()

        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.normal_user,
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
                                      user=self.normal_user,
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
                                      user=self.normal_user,
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
                                      user=self.normal_user,
                                      value_str=self.VALUE_STR_DEFAULT)
        upcf.save()

        with self.assertRaises(IntegrityError):
            upcf = UserProfileCustomField(key_name=custom_field,
                                          user=self.normal_user,
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
                                      user=self.normal_user,
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
                                      user=self.normal_user,
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
                                   user=self.normal_user,
                                   value_bool=123).save()

    def test_wrong_type_int_in_bool_0(self):
        custom_field = CustomField(
            id='bool',
            label='Boolean',
            required=True,
            type='bool')
        custom_field.save()
        upcf = UserProfileCustomField(key_name=custom_field,
                                      user=self.normal_user,
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
                                      user=self.normal_user,
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
                                      user=self.normal_user,
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
                                   user=self.normal_user,
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
                                   user=self.normal_user,
                                   value_int=self.VALUE_STR_DEFAULT).save()
