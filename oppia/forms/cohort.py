import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django import forms
from django.utils.translation import gettext_lazy as _

from oppia.constants import STR_DATE_FORMAT
from profile.models import CustomField


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
        required=False,
        error_messages={'invalid': STR_VALID_DATE})
    end_date = forms.CharField(
        required=False,
        error_messages={'invalid': STR_VALID_DATE})
    courses = forms.CharField(
        widget=forms.Textarea(),
        required=False,
        help_text=_("A comma separated list of course codes"))
    criteria_based = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
        help_text=_('Check if the participants of this cohort must be updated based on criteria'))

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

    def save(self):
        pass

    def clean(self):
        cleaned_data = super(CohortForm, self).clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date or end_date:
            try:
                start_date = datetime.datetime.strptime(start_date, STR_DATE_FORMAT)
            except (TypeError, ValueError):
                raise forms.ValidationError(_("Please enter a valid start date"))
            try:
                end_date = datetime.datetime.strptime(end_date, STR_DATE_FORMAT)
            except (TypeError, ValueError):
                raise forms.ValidationError(_("Please enter a valid end date"))

            # check start date before end date
            if start_date > end_date:
                raise forms.ValidationError(
                    _("Start date must be before the end date."))

        return cleaned_data


class CohortCriteriaForm(forms.Form):

    user_profile_field = forms.ChoiceField(required=False)
    user_profile_value = forms.CharField(max_length=150, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []
        custom_fields = CustomField.objects.all().order_by('order')
        for field in custom_fields:
            choices.append((field.id, field.label))
        self.fields['user_profile_field'].choices = choices

        initial = kwargs.get('initial')
        if initial:
            self.fields['user_profile_field'].initial = [initial['user_profile_field']]
