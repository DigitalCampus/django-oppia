# oppia/profile/forms.py

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML
from django import forms
from django.contrib.auth import (authenticate)
from django.urls import reverse
from django.utils.translation import ugettext as _


class DeleteAccountForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}),
                               required=True)
    password = forms.CharField(widget=forms.PasswordInput,
                               error_messages={'required': _(u'Please enter your password.'), },
                               required=True)

    def __init__(self, *args, **kwargs):
        super(DeleteAccountForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse('profile_delete_account')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
            'username',
            'password',
            Div(
                Submit('submit', _(u'Delete Account'), css_class='btn btn-default'),
                HTML("""<a role="button" class="btn btn-default"
                        href="{% url "profile_edit" %}">Cancel</a>"""),
                css_class='col-lg-offset-2 col-lg-4',

            ),
        )

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        user = authenticate(username=username, password=password)
        if user is None or not user.is_active:
            raise forms.ValidationError(_(u"Invalid password. Please try again."))
        return cleaned_data
