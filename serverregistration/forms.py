from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML

from django import forms
from django.urls import reverse
from django.utils.translation import gettext as _

from settings import constants
from settings.models import SettingProperties


class RegisterServerForm(forms.Form):
    server_url = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':
                                      'readonly'}),
        max_length=100,
        min_length=10,
        error_messages={'required': _(u'Please enter a server url.')},
        help_text=_(u'If this is incorrect or blank, please first update the \
         OPPIA_HOSTNAME in the settings in Oppia Admin, then return to this \
         page'))
    include_no_courses = forms.BooleanField(required=False)
    include_no_users = forms.BooleanField(required=False)
    email_notifications = forms.BooleanField(required=False)
    notif_email_address = forms.CharField(
        max_length=200,
        min_length=5,
        required=False,
        label=_(u'Notification email address'))

    def __init__(self, *args, **kwargs):
        super(RegisterServerForm, self).__init__(* args, ** kwargs)

        self.helper = FormHelper()
        self.helper.form_action = reverse('serverregistration:register')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout()

        self.helper.layout.append('server_url')

        self.helper.layout.append(Div(
                HTML("""<h5>"""
                     + _(u'Provide additional course/user data') + """</h5>""")
            ))
        self.helper.layout.extend(['include_no_courses',
                                   'include_no_users'])

        self.helper.layout.append(Div(
                HTML("""<h5>"""
                     + _(u'Get email notifications') + """</h5>""")
            ))
        self.helper.layout.extend(['email_notifications',
                                   'notif_email_address'])

        if SettingProperties.get_bool(constants.OPPIA_SERVER_REGISTERED,
                                      False):
            button_title = _(u'Update registration')
        else:
            button_title = _(u'Register Server')

        self.helper.layout.append(Div(
                    Submit('submit',
                           button_title,
                           css_class='btn btn-default'),
                    css_class='col-lg-offset-2 col-lg-4',
                ),
            )

    def clean(self):
        cleaned_data = self.cleaned_data
        email_notifications = cleaned_data.get("email_notifications")
        notif_email_address = cleaned_data.get("notif_email_address")
        if email_notifications and notif_email_address == '':
            raise forms.ValidationError(
                _(u"Please give an email address for the notifications"))
        return cleaned_data
