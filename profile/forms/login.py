from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML
from django import forms
from django.contrib.auth import (authenticate)
from django.urls import reverse
from django.utils.translation import ugettext as _


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,
                               error_messages={'required': _(u'Please enter a username.')}, )
    password = forms.CharField(widget=forms.PasswordInput,
                               error_messages={'required': _(u'Please enter a password.'), },
                               required=True)
    next = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__( * args, ** kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse('profile_login')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
            'username',
            'password',
            'next',
            Div(
                Submit('submit', _(u'Login'), css_class='btn btn-default'),
                HTML("""<a class="btn btn-default" href="{% url 'profile_reset' %}">""" + _(
                    u'Forgotten password?') + """</a>"""),
                css_class='col-lg-offset-2 col-lg-4',
            ),
        )

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        user = authenticate(username=username, password=password)
        if user is None or not user.is_active:
            raise forms.ValidationError(_(u"Invalid username or password. Please try again."))
        return cleaned_data