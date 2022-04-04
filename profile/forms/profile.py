# oppia/profile/forms.py
import hashlib
import urllib

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from profile.models import CustomField
from profile.forms import helpers

from settings import constants
from settings.models import SettingProperties


class ProfileForm(forms.Form):
    api_key = forms.CharField(widget=forms.TextInput(attrs={'readonly':
                                                            'readonly'}),
                              required=False,
                              help_text=_(u'You cannot edit your API Key.'))
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':
                                                             'readonly'}),
                               required=False,
                               help_text=_(u'You cannot edit your username.'))
    email = forms.CharField(validators=[validate_email],
                            error_messages={'invalid':
                                            (u'Please enter a valid e-mail \
                                             address.')},
                            required=False)
    password = forms.CharField(widget=forms.PasswordInput,
                               required=False,
                               min_length=6,
                               error_messages={
                                   'min_length':
                                   _(u'The new password should be at least 6 \
                                   characters long')})
    password_again = forms.CharField(widget=forms.PasswordInput,
                                     required=False,
                                     min_length=6)
    first_name = forms.CharField(max_length=100,
                                 min_length=2,
                                 required=True)
    last_name = forms.CharField(max_length=100,
                                min_length=2,
                                required=True)
    job_title = forms.CharField(max_length=100, required=False)
    organisation = forms.CharField(max_length=100, required=False)
    phone_number = forms.CharField(max_length=100, required=False)
    exclude_from_reporting = forms.BooleanField(required=False, help_text=_('If checked, the activity from this user will not be taken into account for summary calculations and reports'))

    def __init__(self, allow_edit=True, *args, **kwargs):
        super(ProfileForm, self).__init__(* args, ** kwargs)

        userdata = kwargs.get('initial') \
            if 'initial' in kwargs else kwargs.get('data')
        email = userdata.get('email', None)
        username = userdata.get('username', None)

        helpers.custom_fields(self)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_tag = False
        self.helper.label_class = 'col-lg-2 col-md-3 col-sm-4'
        self.helper.field_class = 'col-lg-5 col-md-8 col-sm-8'

        self.helper.layout = Layout()

        if SettingProperties.get_bool(
                constants.OPPIA_SHOW_GRAVATARS,
                settings.OPPIA_SHOW_GRAVATARS):
            gravatar_url = "https://www.gravatar.com/avatar.php?"
            gravatar_id = hashlib.md5(str(email).encode('utf-8')).hexdigest()
            gravatar_url += urllib.parse.urlencode({
                'gravatar_id': gravatar_id,
                'size': 64
            })
            self.gravatar = FormHelper()
            self.gravatar.form_tag = False
            self.gravatar.layout = Layout(
                Div(
                    HTML("""<label class="control-label col-lg-2">"""
                         + _(u'Photo') + """</label>"""),
                    Div(
                        HTML(mark_safe(
                            '<img src="{0}" alt="gravatar for {1}" \
                            class="gravatar" width="{2}" height="{2}"/>'
                            .format(gravatar_url, username, 64))),
                        HTML("""<br/>"""),
                        HTML("""<a href="https://www.gravatar.com">"""
                             + _(u'Update gravatar') + """</a>"""),
                        css_class="col-lg-4",
                    ),
                    css_class="form-group",
                )
            )

        if not allow_edit:
            # Set fields as read-only if the user is not allow to edit their
            # profile
            for key, field in self.fields.items():
                if not key.startswith('password'):
                    field.widget.attrs.update({'readonly': 'readonly'})

        self.helper.layout.extend(
            ['job_title',
             'organisation',
             'phone_number'])

        custom_fields = CustomField.objects.all().order_by('order')
        for custom_field in custom_fields:
            self.helper.layout.append(custom_field.id)

        self.helper.layout.extend([
            Div(
                HTML("""<h4 class='mt-5 mb-3'>"""
                     + _(u'Change password') + """</h4>"""),
            ),
            Div(HTML("""<div style='clear:both'></div>""")),
            'password',
            'password_again',
            Div(
                Submit('submit',
                       _(u'Save Profile'),
                       css_class='btn btn-default mt-3'),
                css_class='text-center col-lg-offset-2 col-lg-6',
            )])

    def clean(self):
        cleaned_data = self.cleaned_data
        # check email not used by anyone else
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")

        if email and User.objects.exclude(username__exact=username) \
                .filter(email=email).exists():
            raise forms.ValidationError(_(u"Email address already in use"))

        # if password entered then check they are the same
        password = cleaned_data.get("password")
        password_again = cleaned_data.get("password_again")
        if password and password_again and password != password_again:
            raise forms.ValidationError(_(u"Passwords do not match."))

        return cleaned_data
