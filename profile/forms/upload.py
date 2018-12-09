# oppia/profile/forms.py
import hashlib
import urllib

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML, Field, Row, Column
from django import forms
from django.conf import settings
from django.contrib.auth import (authenticate)
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import validate_email
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
class UploadProfileForm(forms.Form):
    upload_file = forms.FileField(
        required=True,
        error_messages={'required': _('Please select a file to upload')}, )

    def __init__(self, *args, **kwargs):
        super(UploadProfileForm, self).__init__( * args, ** kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse('profile_upload')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
            'upload_file',
            Div(
                Submit('submit', _(u'Upload'), css_class='btn btn-default'),
                css_class='col-lg-offset-2 col-lg-4',
            ),
        )