from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django import forms
from django.utils.translation import ugettext_lazy as _


class CohortHelperDiv(Div):
    template = "cohort/helper.html"


class CohortForm(forms.Form):

    STR_VALID_DATE = _(u'Please enter a valid date')

    description = forms.CharField(required=True)
    teachers = forms.CharField(
        widget=forms.Textarea(),
        required=False,
        help_text=_("A comma separated list of usernames"))
    students = forms.CharField(
        widget=forms.Textarea(),
        required=False,
        help_text=_("A comma separated list of usernames"))
    start_date = forms.CharField(
        required=True,
        error_messages={'required': STR_VALID_DATE,
                        'invalid': STR_VALID_DATE})
    end_date = forms.CharField(
        required=True,
        error_messages={'required': STR_VALID_DATE,
                        'invalid': STR_VALID_DATE})
    courses = forms.CharField(
        widget=forms.Textarea(),
        required=False,
        help_text=_("A comma separated list of course codes"))

    def __init__(self, *args, **kwargs):
        super(CohortForm, self).__init__(* args, ** kwargs)
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
                    css_class='d-none'
                ),
            )
