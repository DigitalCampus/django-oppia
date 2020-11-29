import datetime

from django import forms
from oppia.test import OppiaTestCase
from django.utils import timezone
from helpers.forms import dates

from oppia import constants

class DatesHelperTest(OppiaTestCase):

    '''
    DateDiffForm
    '''
    def test_date_diff_form_valid(self):
        form_data = {'start_date': '2019-12-18'}
        form = dates.DateDiffForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_date_diff_form_wrong_param_name(self):
        form_data = {'start': '2019-12-18'}
        form = dates.DateDiffForm(data=form_data)
        self.assertRaises(forms.ValidationError)
        self.assertFalse(form.is_valid())

    def test_date_diff_form_invalid_date(self):
        form_data = {'start_date': '2019-22-22'}
        form = dates.DateDiffForm(data=form_data)
        self.assertRaises(forms.ValidationError)
        self.assertFalse(form.is_valid())

    def test_date_diff_form_no_date(self):
        form_data = {}
        form = dates.DateDiffForm(data=form_data)
        self.assertRaises(forms.ValidationError)
        self.assertFalse(form.is_valid())

    '''
    DateRangeForm
    '''
    def test_date_range_form_valid(self):
        form_data = {'start_date': '2017-12-18', 'end_date': '2018-01-18'}
        form = dates.DateRangeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_date_range_form_start_date_future(self):
        start_date_in_advance = timezone.now() + datetime.timedelta(days=31)
        form_data = {'start_date':
                     start_date_in_advance.strftime(constants.STR_DATE_DISPLAY_FORMAT),
                     'end_date': '2018-01-18'}
        form = dates.DateRangeForm(data=form_data)
        self.assertRaises(forms.ValidationError)
        self.assertFalse(form.is_valid())

    def test_date_range_form_end_date_future(self):
        end_date_in_advance = timezone.now() + datetime.timedelta(days=31)
        form_data = {'start_date': '2017-12-18',
                     'end_date':
                     end_date_in_advance.strftime(constants.STR_DATE_DISPLAY_FORMAT)}
        form = dates.DateRangeForm(data=form_data)
        self.assertRaises(forms.ValidationError)
        self.assertFalse(form.is_valid())

    def test_date_range_form_start_date_after_end_date(self):
        start_date = timezone.now() + datetime.timedelta(days=31)
        end_date = timezone.now()
        form_data = {'start_date': start_date.strftime(constants.STR_DATE_DISPLAY_FORMAT),
                     'end_date': end_date.strftime(constants.STR_DATE_DISPLAY_FORMAT)}
        form = dates.DateRangeForm(data=form_data)
        self.assertRaises(forms.ValidationError)
        self.assertFalse(form.is_valid())

    def test_date_range_start_invalid(self):
        form_data = {'start_date': '2017-22-22', 'end_date': '2018-01-18'}
        form = dates.DateRangeForm(data=form_data)
        self.assertRaises(forms.ValidationError)
        self.assertFalse(form.is_valid())

    def test_date_range_end_invalid(self):
        form_data = {'start_date': '2017-11-18', 'end_date': '2018-22-22'}
        form = dates.DateRangeForm(data=form_data)
        self.assertRaises(forms.ValidationError)
        self.assertFalse(form.is_valid())

    '''
    DateRangeIntervalForm
    '''
    def test_date_range_interval_form_valid(self):
        form_data = {'interval': 'days',
                     'start_date': '2017-12-18',
                     'end_date': '2018-01-18'}
        form = dates.DateRangeIntervalForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_date_range_interval_form_start_date_future(self):
        start_date_in_advance = timezone.now() + datetime.timedelta(days=31)
        form_data = {'start_date':
                     start_date_in_advance.strftime(constants.STR_DATE_DISPLAY_FORMAT),
                     'end_date': '2018-01-18'}
        form = dates.DateRangeIntervalForm(data=form_data)
        self.assertRaises(forms.ValidationError)
        self.assertFalse(form.is_valid())

    def test_date_range_interval_form_end_date_future(self):
        end_date_in_advance = timezone.now() + datetime.timedelta(days=31)
        form_data = {'start_date': '2017-12-18',
                     'end_date':
                     end_date_in_advance.strftime(constants.STR_DATE_DISPLAY_FORMAT)}
        form = dates.DateRangeIntervalForm(data=form_data)
        self.assertRaises(forms.ValidationError)
        self.assertFalse(form.is_valid())

    def test_date_range_interval_form_start_date_after_end_date(self):
        start_date = timezone.now() + datetime.timedelta(days=31)
        end_date = timezone.now()
        form_data = {'start_date': start_date.strftime(constants.STR_DATE_DISPLAY_FORMAT),
                     'end_date': end_date.strftime(constants.STR_DATE_DISPLAY_FORMAT)}
        form = dates.DateRangeIntervalForm(data=form_data)
        self.assertRaises(forms.ValidationError)
        self.assertFalse(form.is_valid())

    def test_date_range_interval_start_invalid(self):
        form_data = {'start_date': '2017-22-22', 'end_date': '2018-01-18'}
        form = dates.DateRangeIntervalForm(data=form_data)
        self.assertRaises(forms.ValidationError)
        self.assertFalse(form.is_valid())

    def test_date_range_interval_end_invalid(self):
        form_data = {'start_date': '2017-11-18', 'end_date': '2018-22-22'}
        form = dates.DateRangeIntervalForm(data=form_data)
        self.assertRaises(forms.ValidationError)
        self.assertFalse(form.is_valid())
