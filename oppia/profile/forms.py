# oppia/profile/forms.py
import hashlib
import urllib

from django import forms
from django.conf import settings
from django.contrib.auth import (authenticate, login, views)
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Layout, Fieldset, ButtonHolder, Submit, Div, HTML

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, 
                               error_messages={'required': _(u'Please enter a username.')},)
    password = forms.CharField(widget=forms.PasswordInput,
                                error_messages={'required': _(u'Please enter a password.'),},      
                                required=True)
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse('profile_login')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
                                    'username',
                                    'password',
                                Div(
                                   Submit('submit', _(u'Login'), css_class='btn btn-default'),
                                   HTML("""<a class="btn btn-default" href="{% url 'profile_reset' %}">"""+_(u'Forgotten password?') + """</a>"""),
                                   css_class='col-lg-offset-2 col-lg-4',
                                ),
        )
       
    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        
        user = authenticate(username=username, password=password)
        if user is None or not user.is_active:
            raise forms.ValidationError( _(u"Invalid username or password. Please try again."))
        return cleaned_data
     
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30, 
                               min_length=4,
                               error_messages={'required': _(u'Please enter a username.')},)
    email = forms.CharField(validators=[validate_email],
                                error_messages={'invalid': _(u'Please enter a valid e-mail address.'),
                                                'required': _(u'Please enter your e-mail address.')},
                                required=True)
    password = forms.CharField(widget=forms.PasswordInput,
                                error_messages={'required': _(u'Please enter a password.'),
                                                'min_length': _(u'Your password should be at least 6 characters long.')},
                                min_length=6,       
                                required=True)
    password_again = forms.CharField(widget=forms.PasswordInput,
                                    min_length=6,
                                    error_messages={'required': _(u'Please enter your password again.'),
                                                    'min_length': _(u'Your password again should be at least 6 characters long.')},
                                    required=True)
    first_name = forms.CharField(max_length=100,
                                    error_messages={'required': _(u'Please enter your first name.'),
                                                    'min_length': _(u'Your first name should be at least 2 characters long.')},
                                    min_length=2,
                                    required=True)
    last_name = forms.CharField(max_length=100,
                                error_messages={'required': _(u'Please enter your last name.'),
                                                'min_length': _(u'Your last name should be at least 2 characters long.')},
                                min_length=2,
                                required=True)
    job_title = forms.CharField(max_length=100,required=False)
    organisation = forms.CharField(max_length=100,required=False)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse('profile_register')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
                                    'username',
                                    'email',
                                    'password',
                                    'password_again',
                                    'first_name',
                                    'last_name',
                                    'job_title',
                                    'organisation',
                                Div(
                                   Submit('submit', _(u'Register'), css_class='btn btn-default'),
                                   css_class='col-lg-offset-2 col-lg-4',
                                ),
        )

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        password_again = cleaned_data.get("password_again")
        username = cleaned_data.get("username")

        # check the username not already used
        num_rows = User.objects.filter(username=username).count()
        if num_rows != 0:
            raise forms.ValidationError( _(u"Username has already been registered, please select another."))
        
        # check the email address not already used
        num_rows = User.objects.filter(email=email).count()
        if num_rows != 0:
            raise forms.ValidationError( _(u"Email has already been registered"))

        # check the password are the same
        if password and password_again:
            if password != password_again:
                raise forms.ValidationError( _(u"Passwords do not match."))

        # Always return the full collection of cleaned data.
        return cleaned_data

class ResetForm(forms.Form):
    username = forms.CharField(max_length=30,
        error_messages={'invalid': _(u'Please enter a username.')},
        required=True)
    
    def __init__(self, *args, **kwargs):
        super(ResetForm, self).__init__(*args, **kwargs)
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
        num_rows = User.objects.filter(username__exact=username).count()
        if num_rows != 1:
            raise forms.ValidationError( _(u"Username not found"))
        return cleaned_data

class ProfileForm(forms.Form):
    api_key = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}),
                               required=False, help_text=_(u'You cannot edit your API Key.'))
    username = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}),
                               required=False, help_text=_(u'You cannot edit your username.'))
    email = forms.CharField(validators=[validate_email],
                            error_messages={'invalid': _(u'Please enter a valid e-mail address.')},
                            required=True)
    password = forms.CharField(widget=forms.PasswordInput,
                               required=False,
                               min_length=6,
                               error_messages={'min_length': _(u'Your new password should be at least 6 characters long')},)
    password_again = forms.CharField(widget=forms.PasswordInput,
                                     required=False,
                                     min_length=6)
    first_name = forms.CharField(max_length=100,
                                 min_length=2,
                                 required=True)
    last_name = forms.CharField(max_length=100,
                                min_length=2,
                                required=True)
    job_title = forms.CharField(max_length=100,required=False)
    organisation = forms.CharField(max_length=100,required=False)
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if len(args) == 1:
            email = args[0]['email']
            username = args[0]['username']
        else:
            kw = kwargs.pop('initial')
            email = kw['email'] 
            username = kw['username'] 
        self.helper = FormHelper()
        self.helper.form_action = reverse('profile_edit')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        if settings.OPPIA_SHOW_GRAVATARS:
            gravatar_url = "https://www.gravatar.com/avatar.php?"
            gravatar_url += urllib.urlencode({
                'gravatar_id':hashlib.md5(email).hexdigest(),
                'size':64
            })
            self.helper.layout = Layout(
                    Div(
                        HTML("""<label class="control-label col-lg-2">"""+_(u'Photo') + """</label>"""),
                        Div(
                            HTML(mark_safe('<img src="{0}" alt="gravatar for {1}" class="gravatar" width="{2}" height="{2}"/>'.format(gravatar_url, username, 64))),
                            HTML("""<br/>"""),
                            HTML("""<a href="https://www.gravatar.com">"""+_(u'Update your gravatar')+"""</a>"""),
                            css_class="col-lg-4",
                        ),
                        css_class="form-group",
                        ),
                    'api_key',
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    'job_title',
                    'organisation',
                    Div(
                        HTML("""<h3>"""+_(u'Change password') + """</h3>"""),
                        ),
                    'password',
                    'password_again',
                    Div(
                       Submit('submit', _(u'Save'), css_class='btn btn-default'),
                       css_class='col-lg-offset-2 col-lg-4',
                    ),
                )
        else:
            self.helper.layout = Layout(
                    'api_key',
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    Div(
                        HTML("""<h3>"""+_(u'Change password') + """</h3>"""),
                        ),
                    'password',
                    'password_again',
                    Div(
                       Submit('submit', _(u'Save'), css_class='btn btn-default'),
                       css_class='col-lg-offset-2 col-lg-4',
                    ),
                )      

        
    def clean(self):
        cleaned_data = self.cleaned_data
        # check email not used by anyone else
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
        num_rows = User.objects.exclude(username__exact=username).filter(email=email).count()
        if num_rows != 0:
            raise forms.ValidationError( _(u"Email address already in use"))
        
        # if password entered then check they are the same
        password = cleaned_data.get("password")
        password_again = cleaned_data.get("password_again")
        if password and password_again:
            if password != password_again:
                raise forms.ValidationError( _(u"Passwords do not match."))
            
        return cleaned_data