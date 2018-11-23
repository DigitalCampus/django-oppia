# oppia/forms.py
import datetime

from crispy_forms.bootstrap import FieldWithButtons
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Row
from django import forms
from django.utils.translation import ugettext_lazy as _

class DateDiffForm(forms.Form):
    start_date = forms.DateField(
        required=True,
        error_messages={'required': _('Please enter a valid date'),
                        'invalid': _('Please enter a valid date')},
    )

    def __init__(self, *args, **kwargs):
        super(DateDiffForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-3'
        self.helper.layout = Layout(
            FieldWithButtons('start_date', Submit('submit', _(u'Go'), css_class='btn btn-default')),
        )


class DateRangeForm(forms.Form):
    start_date = forms.CharField(
        required=True,
        error_messages={'required': _('Please enter a start date'),
                        'invalid': _('Please enter a valid date')})
    end_date = forms.CharField(
        required=True,
        error_messages={'required': _('Please enter an end date'),
                        'invalid': _('Please enter a valid date')})

    def __init__(self, *args, **kwargs):
        super(DateRangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Div('start_date', css_class='date-picker-row-fluid'),
                FieldWithButtons('end_date', Submit('submit', _(u'Go'), css_class='btn btn-default'),
                                 css_class='date-picker-row-fluid'),
            )
        )

    def clean(self):
        cleaned_data = super(DateRangeForm, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        try:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        except TypeError:
            raise forms.ValidationError("Please enter a valid start date.")
        try:
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        except TypeError:
            raise forms.ValidationError("Please enter a valid end date.")

        # check end date on or before today
        if end_date > datetime.datetime.now():
            raise forms.ValidationError("End date can't be in the future.")

        # check start date before end date
        if start_date > end_date:
            raise forms.ValidationError("Start date must be before the end date.")

        return cleaned_data


class DateRangeIntervalForm(forms.Form):
    INTERVALS = (('days', _('days'),), ('months', _('months')),)
    start_date = forms.CharField(
        required=True,
        error_messages={'required': _('Please enter a start date'),
                        'invalid': _('Please enter a valid date')})
    end_date = forms.CharField(
        required=True,
        error_messages={'required': _('Please enter an end date'),
                        'invalid': _('Please enter a valid date')})
    interval = forms.ChoiceField(widget=forms.Select, choices=INTERVALS)

    def __init__(self, *args, **kwargs):
        super(DateRangeIntervalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Div('start_date', css_class='date-picker-row-fluid'),
                Div('end_date', css_class='date-picker-row-fluid'),
                FieldWithButtons('interval', Submit('submit', _(u'Go'), css_class='btn btn-default'),
                                 css_class='date-picker-row-fluid'),
            )
        )

    def clean(self):
        cleaned_data = super(DateRangeIntervalForm, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        try:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        except TypeError:
            raise forms.ValidationError("Please enter a valid start date.")
        try:
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        except TypeError:
            raise forms.ValidationError("Please enter a valid end date.")

        # check end date on or before today
        if end_date > datetime.datetime.now():
            raise forms.ValidationError("End date can't be in the future.")

        # check start date before end date
        if start_date > end_date:
            raise forms.ValidationError("Start date must be before the end date.")

        return cleaned_data