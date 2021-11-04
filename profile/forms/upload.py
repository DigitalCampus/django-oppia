# oppia/profile/forms.py
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from django import forms
from django.urls import reverse
from django.utils.translation import ugettext as _


class UploadProfileForm(forms.Form):
    upload_file = forms.FileField(
        required=True,
        error_messages={'required': _('Please select a file to upload')}, )

    def __init__(self, *args, **kwargs):
        super(UploadProfileForm, self).__init__(* args, ** kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse('profile:upload')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3 col-md-4 col-sm-3'
        self.helper.field_class = 'col-lg-6 col-md-8 col-sm-6'
        self.helper.layout = Layout(
            'upload_file',
            Div(
                Submit('submit', _(u'Upload'), css_class='btn btn-default'),
                css_class='col-lg-offset-2 col-lg-4',
            ),
        )
