# oppia/profile/forms.py

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from django import forms
from django.utils.translation import gettext as _

from profile.forms import helpers
from profile.models import CustomField

CUSTOMFIELDS_SEARCH_PREFIX = 'userprofilecustomfield_'


class UserSearchForm(forms.Form):
    username = forms.CharField(max_length=100, min_length=2, required=False)
    first_name = forms.CharField(max_length=100, min_length=2, required=False)
    last_name = forms.CharField(max_length=100, min_length=2, required=False)
    email = forms.CharField(max_length=100, min_length=2, required=False)
    is_active = forms.BooleanField(initial=False, required=False)
    is_staff = forms.BooleanField(initial=False, required=False)

    start_date = forms.CharField(required=False, label=False)
    end_date = forms.CharField(required=False, label=False)

    def __init__(self, *args, **kwargs):
        super(UserSearchForm, self).__init__(* args, ** kwargs)

        helpers.custom_fields(self,
                              prefix=CUSTOMFIELDS_SEARCH_PREFIX,
                              make_required=False)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = ("col-sm-3 col-md-2 col-lg-2 pr-0 "
                                   "control-label")
        self.helper.field_class = 'col-sm-8 col-md-5 col-lg-5'
        self.helper.form_method = 'GET'
        self.helper.layout = Layout()

        custom_fields = CustomField.objects.all().order_by('order')
        for custom_field in custom_fields:
            custom_field.required = False
            self.helper.layout.append(
                CUSTOMFIELDS_SEARCH_PREFIX+custom_field.id)

        self.helper.layout.append(
            Div(
                Submit('submit', _('Search'), css_class='btn btn-default'),
                css_class='col-lg-7 col-md-7 col-sm-11 text-right',
            )
        )
