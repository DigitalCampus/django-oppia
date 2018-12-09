# oppia/profile/forms.py

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML, Field, Row, Column
from django import forms
from django.utils.translation import ugettext as _

class UserSearchForm(forms.Form):
    username = forms.CharField(max_length=100, min_length=2, required=False)
    first_name = forms.CharField(max_length=100, min_length=2, required=False)
    last_name = forms.CharField(max_length=100, min_length=2, required=False)
    email = forms.CharField(max_length=100, min_length=2, required=False)
    is_active = forms.BooleanField(initial=False, required=False)
    is_staff = forms.BooleanField(initial=False, required=False)

    register_start_date = forms.CharField(required=False, label=False)
    register_end_date = forms.CharField(required=False, label=False)

    def __init__(self, *args, **kwargs):
        super(UserSearchForm, self).__init__( * args, ** kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3 col-md-2 col-lg-2 control-label'
        self.helper.field_class = 'col-sm-8 col-md-5 col-lg-5'
        self.helper.form_method = 'GET'
        self.helper.layout = Layout(
            'username', 'first_name', 'last_name', 'email',
            Row(Div('is_active', css_class='col-sm-4'), Div('is_staff', css_class='col-sm-4')),
            Row(
                Column(HTML('<label>Register date</label>'), css_class=self.helper.label_class),
                Div(HTML('<div class="btn hidden-xs disabled">from</div>'), css_class='date-picker-row-fluid'),
                Column(Field('register_start_date', css_class='date-picker-input'), css_class='date-picker-row-fluid'),
                Div(HTML('<div class="btn hidden-xs disabled">to</div>'), css_class='date-picker-row-fluid'),
                Column(Field('register_end_date', css_class='date-picker-input'), css_class='date-picker-row-fluid'),
            ),
            Div(
                Submit('submit', _('Search'), css_class='btn btn-default'),
                css_class='col-lg-7 col-md-7 col-sm-11 text-right',
            )
        )