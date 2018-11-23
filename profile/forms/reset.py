# oppia/profile/forms.py

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from django import forms
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import ugettext as _


class ResetForm(forms.Form):
    username = forms.CharField(max_length=30,
                               error_messages={'invalid': _(u'Please enter a username or email address.')},
                               required=True)

    def __init__(self, *args, **kwargs):
        super(ResetForm, self).__init__( * args, ** kwargs)
        self.fields['username'].label = "Username or email"
        self.helper = FormHelper()
        self.helper.form_action = reverse('profile_reset')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
            'username',
            Div(
                Submit('submit', _(u'Reset password'), css_class='btn btn-default'),
                css_class='col-lg-offset-2 col-lg-4',
            ),
        )

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get("username")
        try:
            User.objects.get(username__exact=username)
        except User.DoesNotExist:
            try:
                User.objects.get(email__exact=username)
            except User.DoesNotExist:
                raise forms.ValidationError(_(u"Username/email not found"))
        return cleaned_data
