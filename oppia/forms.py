# oppia/forms.py
import datetime
import math

from crispy_forms.bootstrap import FieldWithButtons
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Row, Field
from django import forms
from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from oppia.settings import constants
from oppia.settings.models import SettingProperties


class UploadCourseStep1Form(forms.Form):
    course_file = forms.FileField(
                required=True,
                error_messages={'required': _('Please select a file to upload')}, )

    def __init__(self, *args, **kwargs):
        super(UploadCourseStep1Form, self).__init__( * args, ** kwargs)

        max_upload = SettingProperties.get_int(constants.MAX_UPLOAD_SIZE, settings.OPPIA_MAX_UPLOAD_SIZE)
        self.fields['course_file'].help_text = _('Max size %(size)d Mb') % {'size': int(math.floor(max_upload / 1024 / 1024))}

        self.helper = FormHelper()
        self.helper.form_action = reverse('oppia_upload')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
                'course_file',
                Div(
                   Submit('submit', _(u'Upload'), css_class='btn btn-default'),
                   css_class='col-lg-offset-2 col-lg-4',
                ),
            )

    def clean(self):
        cleaned_data = super(UploadCourseStep1Form, self).clean()
        file = cleaned_data.get("course_file")

        max_upload = SettingProperties.get_int(constants.MAX_UPLOAD_SIZE, settings.OPPIA_MAX_UPLOAD_SIZE)

        if file is not None and file._size > max_upload:
            size = int(math.floor(max_upload / 1024 / 1024))
            raise forms.ValidationError(_("Your file is larger than the maximum allowed (%(size)d Mb). You may want to check your course for large includes, such as images etc.") % {'size': size, })

        if file is not None and file.content_type != 'application/zip' and file.content_type != 'application/x-zip-compressed':
            raise forms.ValidationError(_("You may only upload a zip file"))

        return cleaned_data


class UploadCourseStep2Form(forms.Form):
    tags = forms.CharField(
                help_text=_("A comma separated list of tags to help classify your course"),
                required=True,
                error_messages={'required': _('Please enter at least one tag')}, )
    is_draft = forms.BooleanField(
                help_text=_("Whether this course is only a draft"),
                required=False, )

    def __init__(self, *args, **kwargs):
        super(UploadCourseStep2Form, self).__init__( * args, ** kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
                'tags',
                'is_draft',
                Div(
                   Submit('submit', _(u'Save'), css_class='btn btn-default'),
                   css_class='col-lg-offset-2 col-lg-4',
                ),
            )


class CohortHelperDiv(Div):
    template = "oppia/includes/cohort-helper.html"


class CohortForm(forms.Form):

    description = forms.CharField(required=True)
    teachers = forms.CharField(widget=forms.Textarea(),
                               required=False,
                               help_text=_("A comma separated list of usernames"), )
    students = forms.CharField(widget=forms.Textarea(),
                               required=True,
                               help_text=_("A comma separated list of usernames"), )
    start_date = forms.CharField(required=True,
                                     error_messages={'required': _('Please enter a valid date'),
                                                     'invalid': _('Please enter a valid date')}, )
    end_date = forms.CharField(required=True,
                                    error_messages={'required': _('Please enter a valid date'),
                                                    'invalid': _('Please enter a valid date')}, )
    courses = forms.CharField(widget=forms.Textarea(),
                              required=False,
                              help_text=_("A comma separated list of course codes"), )

    def __init__(self, *args, **kwargs):
        super(CohortForm, self).__init__( * args, ** kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
        self.helper.label_class = 'col-sm-3 col-md-2'
        self.helper.field_class = 'col-sm-9 col-md-10 col-lg-9'
        self.helper.layout = Layout(
                'description',
                Div('start_date', css_class='date-picker-row'),
                Div('end_date', css_class='date-picker-row'),
                Div(
                    'courses',
                    'teachers',
                    'students',
                    css_class='hidden-fields'
                ),
            )

    
class DateDiffForm(forms.Form):
    start_date = forms.DateField(
        required=True,
        error_messages={'required': _('Please enter a valid date'),
                         'invalid': _('Please enter a valid date')},
        )

    def __init__(self, *args, **kwargs):
        super(DateDiffForm, self).__init__( * args, ** kwargs)
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
        super(DateRangeForm, self).__init__( * args, ** kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                Row(
                    Div('start_date', css_class='date-picker-row-fluid'),
                    FieldWithButtons('end_date', Submit('submit', _(u'Go'), css_class='btn btn-default'), css_class='date-picker-row-fluid'),
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
    INTERVALS = (('days', _('days'), ), ('months', _('months')), )
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
        super(DateRangeIntervalForm, self).__init__( * args, ** kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                Row(
                    Div('start_date', css_class='date-picker-row-fluid'),
                    Div('end_date', css_class='date-picker-row-fluid'),
                    FieldWithButtons('interval', Submit('submit', _(u'Go'), css_class='btn btn-default'), css_class='date-picker-row-fluid'),
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
