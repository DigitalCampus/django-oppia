from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML

from django import forms
from django.urls import reverse
from django.utils.translation import ugettext as _

class RegisterServerForm(forms.Form):
    server_url = forms.CharField(widget=forms.TextInput(attrs={'readonly':
                                                               'readonly'}),
                                 max_length=100,
                                 min_length=10,
                                 error_messages={'required':
                                   _(u'Please enter a server url.')})
    include_no_courses = forms.BooleanField(required=False)
    include_no_users = forms.BooleanField(required=False)
    email_notifications = forms.BooleanField(required=False)
    notif_email_address = forms.CharField(max_length=200,
                                          min_length=5,
                                          required=False)
    
    
    def __init__(self, *args, **kwargs):
        super(RegisterServerForm, self).__init__(* args, ** kwargs)

        self.helper = FormHelper()
        self.helper.form_action = reverse('serverregistration:register')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout()
        
        self.helper.layout.append('server_url')
        
        self.helper.layout.extend(
            ['include_no_courses',
            'include_no_users'])
            
        self.helper.layout.extend(    
            ['email_notifications',
            'notif_email_address']
            )
        self.helper.layout.append(Div(
                Submit('submit', _(u'Register Server'), css_class='btn btn-default'),
                css_class='col-lg-offset-2 col-lg-4',
            ),
        )

    def clean(self):
        cleaned_data = self.cleaned_data
       
        return cleaned_data