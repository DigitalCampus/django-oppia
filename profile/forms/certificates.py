
from django import forms
from django.utils.translation import gettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div

from settings import constants
from settings.models import SettingProperties


class RegenerateCertificatesForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(), required=False)
    old_email = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(RegenerateCertificatesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        if SettingProperties.get_bool(
                constants.OPPIA_EMAIL_CERTIFICATES, False):
            self.helper.layout = Layout(
                'email',
                'old_email',
                Div(
                    Submit('submit',
                           _(u'Regenerate Certificates'),
                           css_class='btn btn-default'),
                    css_class='col-lg-offset-2 col-lg-4'
                ),
            )
        else:
            self.helper.layout = Layout(
                Div(
                    Submit('submit',
                           _(u'Regenerate Certificates'),
                           css_class='btn btn-default'),
                    css_class='col-lg-offset-2 col-lg-4',
                ))
